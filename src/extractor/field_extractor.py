from typing import List, Dict, Any


def split_sections(lines: List[str], section_titles: List[str]) -> Dict[str, Any]:
    """Split lines into sections based on exact matches in section_titles. Returns dict: {section: [lines_or_subsections]}."""
    sections: Dict[str, Any] = {}
    current = None
    for line in lines:
        if line in section_titles:
            current = line
            sections[current] = []
            continue
        if current:
            if line.isupper():
                sections[current].append({"subheading": line, "content": []})
            else:
                if sections[current]:
                    last = sections[current][-1]
                    if isinstance(last, dict) and "subheading" in last:
                        last["content"].append(line)
                    else:
                        sections[current].append(line)
                else:
                    sections[current].append(line)
    return sections


def extract_fields_from_text(lines: List[str], config: Dict[str, Any]) -> Dict[str, Any]:
    """Use split_sections to extract all hardcoded sections into JSON-friendly dict."""
    section_titles = config.get("parser", {}).get("pdf", {}).get("section_titles", [])
    sections = split_sections(lines, section_titles)
    return sections


def extract_fields_from_xlsx_lines(lines: List[str], config: Dict[str, Any]) -> Dict[str, Any]:
    """Fallback: extract from lines if needed."""
    section_titles = config.get("parser", {}).get("xlsx", {}).get("section_titles", [])
    from src.parser.xlsx_parser import extract_xlsx_sections
    # In this fallback, lines not used; call extract_xlsx_sections
    return extract_xlsx_sections(lines[0] if False else config.get('current_xlsx_path', ''), section_titles)


def extract_fields_from_xlsx(xlsx_path: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Primary extraction for XLSX: returns sections grouped by headings and subheadings."""
    section_titles = config.get("parser", {}).get("xlsx", {}).get("section_titles", [])
    from src.parser.xlsx_parser import extract_xlsx_sections
    return extract_xlsx_sections(xlsx_path, section_titles)