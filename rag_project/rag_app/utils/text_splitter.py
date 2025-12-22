from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.documents import Document

def split_text(pages_data: list[dict], chunk_size=500, chunk_overlap=50) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    documents = []
    for page_info in pages_data:
        text = page_info["text"]
        page_num = page_info["page"]
        
        # Split the text of this specific page
        chunks = splitter.split_text(text)
        
        # Create Documents for each chunk, attaching page number
        for chunk in chunks:
            documents.append(Document(
                page_content=chunk,
                metadata={"page": page_num}
            ))
            
    return documents

