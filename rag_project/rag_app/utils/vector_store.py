# vector_store.py
import os
from langchain_chroma import Chroma
from langchain_core.documents import Document
from .embeddings import get_embeddings

DB_PATH = "./chroma_db_data"

def get_vectorstore():
    """Returns the singleton vector store instance."""
    embedding_func = get_embeddings()
    return Chroma(
        collection_name="rag_collection",
        embedding_function=embedding_func,
        persist_directory=DB_PATH
    )

def create_vector_store(documents: list[Document], pdf_id: int):
    """Adds pre-created documents to the vector store, attaching the PDF ID."""
    vectorstore = get_vectorstore()
    
    # Inject pdf_id into each document's metadata
    for doc in documents:
        doc.metadata["pdf_id"] = pdf_id
    
    vectorstore.add_documents(documents)

def delete_from_vector_store(pdf_id: int):
    """Deletes all chunks belonging to a specific PDF."""
    vectorstore = get_vectorstore()
    
    # Chroma doesn't have a simple "delete by metadata" in all versions yet,
    # but we can get IDs by metadata and delete them.
    # Note: This implementation depends on your specific Chroma version.
    # A generic safe way for simple apps is often just checking the metadata matches.
    
    # 1. Get all data
    data = vectorstore.get()
    
    ids_to_delete = []
    if data and "ids" in data and "metadatas" in data:
        for doc_id, meta in zip(data["ids"], data["metadatas"]):
            if meta.get("pdf_id") == pdf_id:
                ids_to_delete.append(doc_id)
                
    if ids_to_delete:
        vectorstore.delete(ids=ids_to_delete)