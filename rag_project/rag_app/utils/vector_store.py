import os
from langchain_community.vectorstores import FAISS
from .embeddings import get_embeddings

def create_vector_store(chunks):
    embeddings = get_embeddings()
    vectorstore = FAISS.from_texts(chunks, embeddings)
    vectorstore.save_local("faiss_index")

def load_vector_store():
    embeddings = get_embeddings()
    index_path = "faiss_index/index.faiss"
    if not os.path.exists(index_path):
        return None
    return FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
