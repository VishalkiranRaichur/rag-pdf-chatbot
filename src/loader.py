def load_pdf(file_path: str) -> str:
    """
    Reads a PDF file and returns all extracted text as one string.
    Uses PyMuPDF (fitz) for fast, reliable extraction.
    """
    try:
        import fitz
    except ImportError as e:
        raise RuntimeError(
            "PyMuPDF is not installed. Run: pip install pymupdf"
        ) from e

    print(f"[DEBUG] Opening PDF: {file_path}", flush=True)

    try:
        doc = fitz.open(file_path)
        text_parts = []

        for page_num, page in enumerate(doc, start=1):
            page_text = page.get_text()
            if page_text:
                text_parts.append(page_text)
            print(f"[DEBUG] Extracted page {page_num}/{len(doc)}", flush=True)

        doc.close()
        text = "\n".join(text_parts)

        if not text.strip():
            raise RuntimeError(
                "No text could be extracted from this PDF. "
                "It may be a scanned image-only document."
            )

        print(f"[DEBUG] PDF extraction finished: {len(text)} characters", flush=True)
        return text

    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError(f"PDF extraction failed: {e}") from e
