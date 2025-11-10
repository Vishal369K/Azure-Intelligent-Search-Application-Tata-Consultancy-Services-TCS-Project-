import re
from docx import Document
from PyPDF2 import PdfReader

def extract_docx_text(file_path: str) -> str:
    doc = Document(file_path)
    text = "\n".join([p.text.strip() for p in doc.paragraphs if p.text.strip()])
    return text

def extract_pdf_text(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_sections(text: str) -> dict:
    sections = {
        "purpose": "",
        "scope": "",
        "responsibilities": "",
        "policy": "",
        "retention": "",
        "disciplinary_actions": ""
    }

    for key in sections.keys():
        pattern = rf"{key}[\s\n:]+(.*?)(?=\n[A-Z][a-zA-Z\s]+:|$)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            sections[key] = match.group(1).strip()

    return sections
