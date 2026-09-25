import pymupdf


def extract_pages(pdf_path: str):
    """
    Extract text from every page of a PDF.

    Returns:
        [
            {
                "page": 1,
                "text": "..."
            },
            ...
        ]
    """

    pages = []

    document = pymupdf.open(pdf_path)

    for page_number, page in enumerate(document, start=1):

        text = page.get_text("text", sort=True)

        text = text.strip()

        if text:
            pages.append({
                "page": page_number,
                "text": text
            })

    document.close()

    return pages