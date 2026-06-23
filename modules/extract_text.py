import pdfplumber
import docx


def extract_text_from_pdf(filepath):
    """Extract raw text from a PDF file."""
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_text_from_docx(filepath):
    """Extract raw text from a DOCX file."""
    doc = docx.Document(filepath)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


def extract_text(filepath):
    """Detect file type from its extension and extract text accordingly."""
    if filepath.lower().endswith('.pdf'):
        return extract_text_from_pdf(filepath)
    elif filepath.lower().endswith('.docx'):
        return extract_text_from_docx(filepath)
    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX are supported.")