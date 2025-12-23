import os
import re # For robust JSON extraction
import json  # Required for parsing LLM output
import shutil
from io import BytesIO

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.files.base import ContentFile

# Requires: pip install pymupdf (fitz)
import fitz # PyMuPDF

from .models import UploadedPDF, PDFPage
from .utils.pdf_loader import extract_text_from_pdf
from .utils.text_splitter import split_text
from .utils.vector_store import create_vector_store, get_vectorstore, delete_from_vector_store
from .utils.llm import get_llm


def upload_pdf(request):
    """
    Handle PDF upload, text extraction, vector store creation,
    and generating images for EVERY page (for visual citations).
    """
    msg = None
    if request.method == "POST":
        files = request.FILES.getlist("pdfs")
        for pdf_file in files:
            # 1. Save PDF in DB
            pdf_obj = UploadedPDF.objects.create(file=pdf_file)

            # 2. Extract text and create vector store
            pages_data = extract_text_from_pdf(pdf_obj.file.path)
            documents = split_text(pages_data)
            create_vector_store(documents, pdf_obj.id)

            # 3. Generate Images for EVERY Page
            try:
                # Use PyMuPDF (fitz) instead of pdf2image to avoid Poppler dependency
                doc = fitz.open(pdf_obj.file.path)
                
                for i, page in enumerate(doc):
                    page_number = i + 1
                    
                    # Render page to image (pixmap)
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # 2x zoom for better quality
                    img_data = pix.tobytes("jpg")
                    
                    page_obj = PDFPage(pdf=pdf_obj, page_number=page_number)
                    file_name = f"{pdf_obj.id}_page_{page_number}.jpg"
                    
                    # Save directly from bytes
                    page_obj.image.save(file_name, ContentFile(img_data), save=True)

                    if page_number == 1:
                        pdf_obj.cover_image = page_obj.image
                        pdf_obj.save()
                        
                doc.close()
                        
            except Exception as e:
                print(f"⚠️ Could not process PDF images: {e}")

        msg = f"{len(files)} PDF(s) processed successfully"

    pdfs = UploadedPDF.objects.all().order_by('-uploaded_at')
    return render(request, "rag_app/upload.html", {"msg": msg, "pdfs": pdfs})


def ask_question(request):
    """
    Handle Q&A. Returns a STRUCTURED JSON object (Title, Subtitle, Content, Points).
    """
    question = request.GET.get("q")
    pdf_id = request.GET.get("pdf_id")

    if not question:
        return JsonResponse({"error": "Question is required"}, status=400)

    try:
        vectorstore = get_vectorstore()
        search_kwargs = {"k": 6}

        if pdf_id != "all":
            search_kwargs["filter"] = {"pdf_id": int(pdf_id)}

        docs = vectorstore.similarity_search(question, **search_kwargs)

        if not docs:
            return JsonResponse({
                "answer": {
                    "title": "No Info Found", 
                    "subtitle": "Search Result", 
                    "content": "I couldn't find relevant information in the uploaded documents.", 
                    "points": []
                }
            })

        # --- Retrieve specific page image ---
        source_image_url = None
        best_doc = docs[0]
        
        # Get metadata safely
        matched_pdf_id = best_doc.metadata.get('pdf_id') 
        # Metadata 'page' is now 1-based from our new loader
        source_page_num = best_doc.metadata.get('page', 1)
        
        try:
            if matched_pdf_id:
                page_obj = PDFPage.objects.filter(
                    pdf_id=matched_pdf_id, 
                    page_number=source_page_num
                ).first()
                if page_obj and page_obj.image:
                    source_image_url = page_obj.image.url
        except Exception as e:
            print(f"Error fetching source image: {e}")

        # --- Generate Answer in Semantic Format ---
        # Add page numbers to context for the LLM
        context = ""
        for doc in docs:
            p_num = doc.metadata.get('page', '?')
            context += f"[Page {p_num}] {doc.page_content}\n\n"

        llm = get_llm()
        
        # Explicit JSON Prompt with Strict Context Rules
        prompt = f"""You are a strict AI assistant designed to answer questions based ONLY on the provided context from a PDF document.

**CRITICAL INSTRUCTIONS:**
1.  **NO OUTSIDE KNOWLEDGE:** Do not use your own knowledge. If the answer is not explicitly in the Context below, you MUST say "I cannot find the answer in the document."
2.  **JSON ONLY:** Output your answer in valid JSON format.
3.  **JSON STRUCTURE:**
    {{
        "title": "A short headline",
        "subtitle": "Context summary",
        "content": "The answer found in the text. if not found, say 'I cannot find the answer in the document.'",
        "points": ["Key point 1", "Key point 2"] (optional, can be empty)
    }}

Context:
{context}

Question: {question}
"""

        response = llm.invoke(prompt)
        raw_answer = getattr(response, "content", str(response))

        # --- Robust JSON Extraction ---
        try:
            # Look for something that starts with { and ends with } (including newlines)
            match = re.search(r'\{.*\}', raw_answer, re.DOTALL)
            if match:
                cleaned_answer = match.group(0)
                answer_json = json.loads(cleaned_answer)
            else:
                raise ValueError("No JSON object found")
                
        except (json.JSONDecodeError, ValueError) as e:
            print(f"JSON Parse Error: {e}. Raw output: {raw_answer}")
            answer_json = {
                "title": "Answer",
                "subtitle": "Generated Response",
                "content": raw_answer, # Fallback to showing whatever the model spit out
                "points": []
            }

        # Get source PDF details
        source_pdf_url = ""
        
        # LOGIC CHANGE: Only provide source if the answer was actually found
        # We check for the specific phrase the prompt is instructed to use.
        ans_content = answer_json.get("content", "").lower()
        if "cannot find the answer" in ans_content:
            # Answer not found, suppress source link
            source_pdf_url = ""
            source_page_num = None
        elif matched_pdf_id:
            try:
                pdf_obj = UploadedPDF.objects.get(id=matched_pdf_id)
                if pdf_obj.file:
                    source_pdf_url = pdf_obj.file.url
            except UploadedPDF.DoesNotExist:
                pass

        return JsonResponse({
            "answer": answer_json,
            "source_image": source_image_url,
            "pdf_url": source_pdf_url,
            "page_number": source_page_num
        })

    except Exception as e:
        print(f"❌ Error: {e}")
        return JsonResponse({"answer": {"title": "Error", "content": "Server Error occurred"}}, status=500)


def delete_pdf(request, pdf_id):
    try:
        pdf = get_object_or_404(UploadedPDF, id=pdf_id)
        if pdf.file:
            pdf.file.delete(save=False)
        pdf.delete()
        delete_from_vector_store(pdf_id)
    except Exception as e:
        print(f"Error deleting PDF: {e}")
    return redirect("upload_pdf")


def download_transcript(request, pdf_id):
    """
    Generate and download a text transcript of the PDF.
    """
    pdf = get_object_or_404(UploadedPDF, id=pdf_id)
    
    try:
        pages_data = extract_text_from_pdf(pdf.file.path)
        full_text = f"Transcript for: {pdf.filename}\n"
        full_text += f"Uploaded: {pdf.uploaded_at}\n"
        full_text += "="*50 + "\n\n"
        
        for data in pages_data:
            full_text += f"--- Page {data['page']} ---\n"
            full_text += data['text'] + "\n\n"
            
        response = HttpResponse(full_text, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="transcript_{pdf.filename}.txt"'
        return response
        
    except Exception as e:
        print(f"Error generating transcript: {e}")
        return HttpResponse("Error generating transcript", status=500)


def home(request):
    return render(request, "rag_app/home.html")