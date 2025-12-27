from pypdf import PdfReader

def extract_text_from_pdf(file):
    """
    Extract full text from resume PDF
    """
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()


def extract_relevant_resume_text(text):
    """
    Keep only relevant resume sections to avoid noise.
    This improves ML similarity scores.
    """
    keywords = ["skills", "projects", "experience", "internship"]
    lines = text.lower().split("\n")

    relevant_lines = []
    keep = False

    for line in lines:
        if any(keyword in line for keyword in keywords):
            keep = True
        if keep:
            relevant_lines.append(line)

    # fallback if nothing detected
    if not relevant_lines:
        return text

    return " ".join(relevant_lines)