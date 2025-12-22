import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    """
    Extracts text from a PDF, preserving page numbers.
    Returns: [{"text": "...", "page": 1}, ...]
    """
    pages_data = []

    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        text = page.get_text()
        if text.strip():  # Only add pages with text
            pages_data.append({"text": text, "page": i + 1}) # 1-based indexing

    return pages_data
