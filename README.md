# 📚 Django RAG PDF Q&A Project

A simple Retrieval-Augmented Generation (RAG) system built with **Django**, **FAISS**, and **Ollama (LLaMA 3)**.  
It allows users to upload PDFs, automatically indexes their content into a vector store, and then ask natural language questions about the document.

---

## 🚀 Features
- **PDF Ingestion**: Upload PDF files via a simple web interface.
- **Text Processing**: Automatically extracts text and splits it into manageable chunks.
- **Vector Storage**: Stores embeddings in a local **FAISS** vector database.
- **AI Answering**: Uses **Ollama (LLaMA 3)** running locally to generate context-aware answers.

---

## 🛠️ Tech Stack
- **Django 5.x** – Web framework
- **LangChain** – LLM Orchestration
- **FAISS** – Vector store for similarity search
- **HuggingFace Transformers** – Embedding generation
- **Ollama** – Local LLM runner
- **PyMuPDF** – PDF parsing

---

## ⚙️ Installation

### Prerequisites
Ensure you have **Python 3.10+** and **Ollama** installed on your system.

### 1. Clone the repository
```bash
git clone [https://github.com/your-username/rag_project.git](https://github.com/your-username/rag_project.git)
cd rag_project

2. Set up Virtual Environment
Bash

# Create virtual environment named 'tfenv'
python -m venv tfenv

# Activate on Linux/Mac
source tfenv/bin/activate

# Activate on Windows
tfenv\Scripts\activate

3. Install Dependencies
Bash

pip install -r requirements.txt

4. Setup Database
Bash

python manage.py migrate

5. Setup Ollama
Make sure Ollama is installed and pull the LLaMA 3 model:

Bash

ollama pull llama3

6. Run the Server
Bash

python manage.py runserver

📂 Project Structure
rag_project/
├── rag_app/
│   ├── templates/rag_app/
│   │   ├── base.html
│   │   └── upload.html
│   ├── static/rag_app/css/
│   │   └── style.css
│   ├── utils/
│   │   ├── pdf_loader.py
│   │   ├── text_splitter.py
│   │   ├── vector_store.py
│   │   └── embeddings.py
│   ├── views.py
│   ├── models.py
│   └── urls.py
├── rag_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── README.md

📖 Usage
Start Ollama: Open a separate terminal and ensure Ollama is running (ollama serve).

Open Browser: Go to http://127.0.0.1:8000/.

Upload: Use the interface to upload a PDF document.

Ask: Type a question related to the PDF content in the input box.

View Results: The system will retrieve relevant context and generate an answer.

📝 Notes & Troubleshooting
Ollama Error: If you get a connection error, ensure Ollama is running on port 11434.

FAISS Index: The vector store is saved locally in the faiss_index/ directory. If you want to reset the knowledge base, simply delete this folder and re-upload your PDF.

Production: This project uses DEBUG=True and SQLite. For production, configure .env variables and switch to PostgreSQL.
