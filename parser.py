import fitz
from docx import Document


def extract_text_from_pdf(file):
    document = fitz.open(stream=file.read(), filetype="pdf")

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


def extract_text_from_docx(file):
    document = Document(file)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def extract_text(file):

    if file.name.endswith(".pdf"):
        return extract_text_from_pdf(file)

    elif file.name.endswith(".docx"):
        return extract_text_from_docx(file)

    else:
        raise ValueError("Unsupported file format")