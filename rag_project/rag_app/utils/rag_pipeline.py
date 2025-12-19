from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from rag_app.utils.llm import get_llm
from rag_app.utils.vector_store import load_vector_store


def get_answer(question: str) -> str:
    llm = get_llm()
    vectorstore = load_vector_store()

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant.
Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}
""")

    def retrieve_context(question: str):
        docs = retriever.get_relevant_documents(question)
        return "\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {
            "context": retrieve_context,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
    )

    response = rag_chain.invoke(question)
    return response.content
