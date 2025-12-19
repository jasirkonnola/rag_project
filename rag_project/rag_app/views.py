# views.py
import shutil
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import UploadedPDF
from .utils.pdf_loader import extract_text_from_pdf
from .utils.text_splitter import split_text
from .utils.vector_store import create_vector_store, get_vectorstore, delete_from_vector_store
from .utils.llm import get_llm

def upload_pdf(request):
    msg = None
    if request.method == "POST":
        files = request.FILES.getlist("pdfs")
        for pdf in files:
            obj = UploadedPDF.objects.create(file=pdf)
            text = extract_text_from_pdf(obj.file.path)
            chunks = split_text(text)
            # We now pass the ID so it's stored in metadata
            create_vector_store(chunks, obj.id)
        msg = f"{len(files)} PDF(s) processed successfully"
    
    pdfs = UploadedPDF.objects.all()
    return render(request, "rag_app/upload.html", {"msg": msg, "pdfs": pdfs})

def ask_question(request):
    question = request.GET.get("q")
    pdf_id = request.GET.get("pdf_id")

    if not question:
        return JsonResponse({"error": "Question is required"}, status=400)

    try:
        vectorstore = get_vectorstore()
        
        # FIX 1: Increase 'k' to get more context (read more parts of the PDF)
        search_kwargs = {"k": 6} 
        
        if pdf_id != "all":
            search_kwargs["filter"] = {"pdf_id": int(pdf_id)}
            
        docs = vectorstore.similarity_search(question, **search_kwargs)

        if not docs:
            return JsonResponse({"answer": "I don't know (no info found)"})

        context = "\n\n".join(doc.page_content for doc in docs)
        
        llm = get_llm()
        
        # FIX 2: Better Prompt Engineering
        # We explicitly ask for "detailed," "comprehensive," and "bullet points."
        prompt = f"""You are an expert AI assistant. 
Your task is to provide a detailed and comprehensive answer based strictly on the context below.

Instructions:
1. Elaborate on the key points. Do not give one-line answers.
2. Use bullet points or numbered lists to organize information.
3. If the context contains steps or specific details, list them all.
4. If the answer is not in the context, say "I don't know".

Context:
{context}

Question: {question}

Detailed Answer:"""
        
        response = llm.invoke(prompt)
        answer = getattr(response, "content", str(response))
        
        return JsonResponse({"answer": answer})

    except Exception as e:
        print(f"❌ Error: {e}")
        return JsonResponse({"answer": "Error occurred on server"}, status=500)
    
def delete_pdf(request, pdf_id):
    try:
        pdf = UploadedPDF.objects.get(id=pdf_id)
        pdf.file.delete(save=False)
        pdf.delete()
        # Remove specific chunks from the single vector store
        delete_from_vector_store(pdf_id)
    except UploadedPDF.DoesNotExist:
        pass
    return redirect("upload_pdf")