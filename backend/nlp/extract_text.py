import pdfplumber
import docx

def extract_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file using pdfplumber.
    """
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_from_docx(file_path: str) -> str:
    """
    Extract text from a DOCX file using python-docx.
    """
    doc = docx.Document(file_path)
    text = " ".join([para.text for para in doc.paragraphs])
    return text

def extract_resume(file_path: str) -> str:
    """
    Unified function: detects file type and extracts text.
    """
    if file_path.lower().endswith(".pdf"):
        return extract_from_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        return extract_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Use PDF or DOCX.")
