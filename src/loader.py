from pypdf import PdfReader


def load_pdf(file_path: str) -> str:
    """
    Reads a PDF file and returns all extracted text as one string.
    """
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text