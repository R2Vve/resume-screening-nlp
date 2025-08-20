import os
import re
from typing import Dict, List, Optional
import docx
import PyPDF2

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
    except Exception:
        # Gracefully degrade
        return ""
    return text

def extract_text_from_docx(file_path: str) -> str:
    try:
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception:
        return ""

def extract_text_from_txt(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as f:
            return f.read()
    except Exception:
        return ""

def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    if ext == ".docx":
        return extract_text_from_docx(file_path)
    if ext == ".txt":
        return extract_text_from_txt(file_path)
    return ""

def clean_text(text: str) -> str:
    # Preserve emails, phones, and punctuation while normalizing whitespace
    text = re.sub(r"\r\n|\r|\n", " ", text)
    text = re.sub(r"\s+", " ", text)
    # Remove excessive non-printable characters
    text = re.sub(r"[^\x09\x0A\x0D\x20-\x7E]", " ", text)
    return text.strip()

def load_resumes(resume_dir: str) -> List[Dict]:
    items: List[Dict] = []
    for filename in os.listdir(resume_dir):
        path = os.path.join(resume_dir, filename)
        if not os.path.isfile(path):
            continue
        if os.path.splitext(filename)[1].lower() not in ALLOWED_EXTENSIONS:
            continue
        raw = extract_text(path)
        cleaned = clean_text(raw)
        items.append({"name": filename, "text": cleaned})
    return items