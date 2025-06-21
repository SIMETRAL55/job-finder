import pandas as pd
from typing import List, Dict, Any


def extract_xlsx_sections(xlsx_path: str, section_titles: List[str]) -> Dict[str, Any]:
    """Extract sections from the first sheet of XLSX based on section_titles.
    Each section starts when a cell in first column exactly matches a title; collects rows until next title.
    Handles subheadings: if first column non-empty and not a main section title, treat as subheading under current section.
    Stores rows of content under section/subheading."""
    # Read first sheet
    xls = pd.ExcelFile(xlsx_path)
    sheet = xls.sheet_names[0]
    df = pd.read_excel(xlsx_path, sheet_name=sheet, header=None, dtype=str)
    df = df.fillna("")
    sections: Dict[str, Any] = {}
    current_section = None
    for idx, row in df.iterrows():
        first = str(row.iloc[0]).strip()
        # Check if this row indicates a main section
        if first in section_titles:
            current_section = first
            sections[current_section] = []
            continue
        if current_section is None:
            # Skip rows before first section or optionally collect under 'metadata'
            continue
        # Now within a section
        # Check for subheading: non-empty first cell not matching main title
        if first:
            # Treat as subheading
            sub = {"subheading": first, "content": []}
            sections[current_section].append(sub)
            # Append any additional cells in this row as first content line
            row_vals = [str(cell).strip() for cell in row.iloc[1:].tolist() if str(cell).strip()]
            if row_vals:
                sub["content"].append(" ".join(row_vals))
        else:
            # Content row: append to last subheading if exists, else as direct content under section
            row_vals = [str(cell).strip() for cell in row.tolist() if str(cell).strip()]
            if not row_vals:
                continue
            if sections[current_section] and isinstance(sections[current_section][-1], dict):
                sections[current_section][-1]["content"].append(" ".join(row_vals))
            else:
                # Direct content
                sections[current_section].append(" ".join(row_vals))
    return sections


def extract_lines_from_xlsx(xlsx_path: str) -> List[str]:
    # Deprecated: not used when using extract_xlsx_sections
    lines = []
    xls = pd.ExcelFile(xlsx_path)
    for sheet in xls.sheet_names:
        try:
            df = pd.read_excel(xlsx_path, sheet_name=sheet, header=None, dtype=str)
        except Exception:
            continue
        df = df.fillna("")
        for idx, row in df.iterrows():
            first = str(row.iloc[0]).strip()
            if first:
                lines.append(first)
    return lines