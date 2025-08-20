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

def load_resumes(directory: str) -> List[Dict[str, str]]:
    """Load all resumes from the given directory.
    
    Args:
        directory: Path to directory containing resume files
        
    Returns:
        List of dicts with 'filename' and 'text' keys
    """
    resumes = []
    for filename in os.listdir(directory):
        if os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS:
            filepath = os.path.join(directory, filename)
            try:
                text = extract_text(filepath)
                cleaned = clean_text(text)
                resumes.append({"filename": filename, "text": cleaned})
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    return resumes