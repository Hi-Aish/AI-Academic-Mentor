def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200):
    """
    Split text into overlapping chunks.

    chunk_size:
        Approximate number of characters per chunk.
    overlap:
        Number of characters repeated between adjacent chunks to maintain context.
    """

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def chunk_pages(pages):
    """
    Convert page-level text into chunks while preserving page metadata.
    """

    chunks = []

    for page_data in pages:
        page_number = page_data["page"]
        text = page_data["text"]

        page_chunks = chunk_text(text)

        for chunk_index, chunk in enumerate(page_chunks):
            chunks.append({
                "text": chunk,
                "page": page_number,
                "chunk_index": chunk_index
            })

    return chunks