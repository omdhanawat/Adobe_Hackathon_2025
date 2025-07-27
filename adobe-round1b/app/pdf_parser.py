import fitz  # PyMuPDF

def create_document_sections(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4].strip()
            if len(text) >= 30:
                sections.append({
                    "text": text,
                    "page_number": page_num
                })
    return sections
