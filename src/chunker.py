CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def chunk_text(text: str) -> list[str]:
    """Split text into overlapping chunks using pure Python."""
    print("[DEBUG] chunk_text started", flush=True)
    print(f"[DEBUG] text length: {len(text)}", flush=True)

    if not text or not text.strip():
        print("[DEBUG] chunk count: 0", flush=True)
        return []

    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + CHUNK_SIZE, text_len)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= text_len:
            break
        start = end - CHUNK_OVERLAP

    print(f"[DEBUG] chunk count: {len(chunks)}", flush=True)
    return chunks
