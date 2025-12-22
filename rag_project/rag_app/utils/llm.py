# llm.py
from langchain_ollama import ChatOllama

def get_llm():
    # "llama3.2" is a 3B model optimized for edge devices (much faster)
    # temperature=0 ensures facts are strictly from the context
    # format="json" ensures the model outputs valid JSON locally if supported
    return ChatOllama(model="llama3.2", temperature=0, format="json")