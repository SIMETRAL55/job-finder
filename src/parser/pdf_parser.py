import pdfplumber
from typing import List

def extract_text_lines(pdf_path: str) -> List[str]:
    """Extract text from PDF, return list of stripped lines."""
    lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                for line in text.splitlines():
                    stripped = line.strip()
                    if stripped:
                        lines.append(stripped)
    return lines