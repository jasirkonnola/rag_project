from django.shortcuts import render
from django.http import JsonResponse
from .models import UploadedPDF
from .utils.pdf_loader import extract_text_from_pdf
from .utils.text_splitter import split_text
from .utils.vector_store import create_vector_store, load_vector_store
from .utils.llm import get_llm

def upload_pdf(request):
    pdf_name = None
    msg = None

    if request.method == "POST":
        pdf = request.FILES['pdf']
        obj = UploadedPDF.objects.create(file=pdf)

        text = extract_text_from_pdf(obj.file.path)
        chunks = split_text(text)
        create_vector_store(chunks)

        pdf_name = obj.file.name.split('/')[-1]
        msg = "PDF processed successfully"

    return render(request, "rag_app/upload.html", {"msg": msg, "pdf_name": pdf_name})

def ask_question(request):
    question = request.GET.get("q")
    if not question:
        return JsonResponse({"error": "Question is required"}, status=400)

    try:
        vectorstore = load_vector_store()
        if not vectorstore:
            return JsonResponse({"answer": "No vector store found. Upload a PDF first."})

        docs = vectorstore.similarity_search(question, k=3)
        if not docs:
            return JsonResponse({"answer": "I don't know"})

        context = "\n".join(getattr(d, "page_content", "") for d in docs)

        llm = get_llm()
        response = llm.invoke(
            f"""Answer using ONLY the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}
"""
        )

        # Handle Ollama response safely
        answer = getattr(response, "content", str(response))
        return JsonResponse({"answer": answer})

    except Exception as e:
        print("❌ ask_question error:", e)
        return JsonResponse({"answer": "Error occurred on server"})
