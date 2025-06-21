import os
from pathlib import Path

def detect_file_type(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        return "pdf"
    elif ext in [".xls", ".xlsx"]:
        return "xlsx"
    else:
        # Optionally, try to inspect file binary signature
        raise ValueError(f"Unsupported file type: {ext}")
