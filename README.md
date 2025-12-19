# Local PDF RAG with Auto-Summarization 🦙

A powerful, privacy-focused application that allows you to chat with your PDF documents locally. Built with Django, LangChain, and Ollama, this tool runs entirely on your machine—no data leaves your computer.

It features **automatic summarization** upon upload and uses **metadata filtering** to let you query specific documents or your entire library at once.

## ✨ Features

* **100% Local Processing:** Uses `Ollama` and open-source embedding models. No API keys required.
* **Auto-Summarization:** Automatically generates a 3-5 bullet point summary for every PDF uploaded.
* **Smart Context Retrieval:** Uses `ChromaDB` to store vectors and retrieve the most relevant 6 chunks of text for high-quality answers.
* **Metadata Filtering:** Chat with a specific PDF or search across "All Documents" simultaneously.
* **Optimized Performance:** configured for `Llama 3.2` (3B) and `all-MiniLM-L6-v2` for fast CPU inference.

## 🛠️ Tech Stack

* **Backend Framework:** Django
* **LLM Orchestration:** LangChain
* **Local LLM:** Ollama (Llama 3.2)
* **Vector Database:** ChromaDB
* **Embeddings:** HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
* **PDF Parsing:** PyMuPDF (Fitz)

---

## 📋 Prerequisites

Before running the app, ensure you have the following installed:

1.  **Python 3.10+**
2.  **Ollama:** [Download and install from ollama.com](https://ollama.com/)

### Model Setup
Open your terminal and pull the optimized model (approx. 2GB):

```bash
ollama pull llama3.2

---

📦 Installation Guide
1. Clone the Repository
Bash

git clone <your-repo-url>
cd <your-project-folder>
2. Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.

Windows:

Bash

python -m venv venv
venv\Scripts\activate
Mac/Linux:

Bash

python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Install the required Python packages:

Bash

pip install django langchain langchain-community langchain-huggingface langchain-chroma langchain-ollama sentence-transformers pymupdf
4. Database Setup
Initialize the SQLite database for Django:

Bash

python manage.py migrate
🚀 Usage
1. Start the Server
Bash

python manage.py runserver
2. Access the App
Open your web browser and go to: https://www.google.com/search?q=http://127.0.0.1:8000/

3. Workflow
Upload: Select one or multiple PDF files. The app will extract text, generate embeddings, and create a summary automatically.

Review: See the auto-generated summary in the file list.

Chat: Type a question in the search bar.

Select "All" to search the whole library.

Select a Specific PDF to narrow down the answer.

📂 Project Structure
Ensure your project files are organized as follows for imports to work correctly:

Plaintext

my_project/                   <-- ROOT FOLDER (Open VS Code here)
├── manage.py                 <-- Django command tool
├── db.sqlite3                <-- Database file (created after migrate)
├── chroma_db_data/           <-- (Auto-created folder for vector storage)
│
├── rag_project/              <-- PROJECT CONFIGURATION FOLDER
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py           <-- Add 'rag_app' to INSTALLED_APPS here
│   ├── urls.py               <-- Include 'rag_app.urls' here
│   └── wsgi.py
│
└── rag_app/                  <-- YOUR APP FOLDER
    ├── __init__.py           <-- Empty file (Required)
    ├── admin.py
    ├── apps.py
    ├── models.py             <-- Defines UploadedPDF model
    ├── urls.py               <-- URL patterns for upload/chat
    ├── views.py              <-- Main logic (Upload, Chat, Summarize)
    ├── tests.py
    │
    ├── templates/            <-- HTML FILES
    │   └── rag_app/
    │       └── upload.html
    │
    └── utils/                <-- HELPER SCRIPTS
        ├── __init__.py       <-- Empty file (Required for imports)
        ├── embedding.py      <-- HuggingFace Setup
        ├── llm.py            <-- ChatOllama Setup
        ├── pdf_loader.py     # Extract text from PDF
        ├── text_splitter.py  # Split text into chunks
        └── vector_store.py   # ChromaDB logic

❓ Troubleshooting
Q: Import "rag_app.utils..." could not be resolved

A: Ensure you have an empty __init__.py file inside the rag_app folder and the rag_app/utils folder.

Q: The answers are too slow.

A: Check that you are using llama3.2 in llm.py. If you are using llama3 (8B parameters), it will be significantly slower on a standard laptop CPU.

Q: sqlite3.OperationalError regarding Chroma.

A: If you are on an older version of Python or Windows, you might need to install pysqlite3-binary. However, standard pip install chromadb usually handles this.
