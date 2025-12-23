# RAG PDF Assistant with Split-View

![App Screenshot](https://github.com/jasirkonnola/rag_project/edit/main/rag_project/DocuChat.png)

A sophisticated Django-based RAG (Retrieval-Augmented Generation) application that allows users to chat with their PDF documents. It features a modern **Gemini-style Split View** UI, where source documents are displayed side-by-side with the chat, automatically navigating to the exact page where the answer was found.

## ✨ Key Features

*   **📚 RAG Pipeline**: Upload multiple PDFs and ask questions. The AI retrieves context-aware answers.
*   **🖥️ Split-View Interface**:
    *   **Chat on Left**: Clean, responsive chat interface.
    *   **Source Viewer on Right**: Hidden by default, opens efficiently when needed.
*   **🎯 Deep Linking**: Clicking a citation button ("Source Page 5") opens the **Full PDF** directly to that page using native browser PDF controls (zoom, search, print).
*   **💾 Smart Persistence**:
    *   Chat history is automatically saved to your local browser storage.
    *   Messages persist even if you reload the page or delete a file.
*   **🎨 Pro UI/UX**:
    *   Clean filenames (hidden folders).
    *   Instant delete with no annoying popups.
    *   Modern Tailwind CSS styling.
*   **🔒 Robust Security**:
    *   Secure file handling.
    *   `X-Frame-Options` configured to allow safe iframe embedding.

## 🛠️ Technology Stack

*   **Backend**: Django 5.x, Python 3.10+
*   **AI/RAG**: LangChain, ChromaDB (or FAISS), Google Gemini (or configured LLM).
*   **Frontend**: HTML5, Vanilla JavaScript, Tailwind CSS (CDN).
*   **PDF Engine**: PyMuPDF (`fitz`) for metadata extraction.

## 🚀 Getting Started

### Prerequisites

*   Python 3.10 or higher.
*   `pip` package manager.

### Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd rag_project
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Ensure you have `django`, `langchain`, `google-generativeai`, `pymupdf`, `chromadb`, etc.)*

3.  **Apply Migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4.  **Run the Server**:
    ```bash
    python manage.py runserver
    ```

5.  **Access the App**:
    Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## 📖 Usage Guide

1.  **Upload**: Click the Cloud icon or drag & drop PDFs into the sidebar.
2.  **Chat**: Type your question in the bottom bar.
3.  **View Sources**:
    *   If the AI finds the answer in a PDF, a **"Source Page X"** button will appear.
    *   Click it to split the screen and see the PDF page side-by-side.
    *   Use the arrow icon in the viewer header to open the PDF in a new tab if needed.
4.  **Manage**:
    *   Click the **Trash icon** to instantly delete a document.
    *   Click **"Clear Conversation"** in the sidebar to reset your chat history.


```bash
📂 Project Structure

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
