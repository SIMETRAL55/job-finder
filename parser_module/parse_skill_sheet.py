import argparse
import json
from PyPDF2 import PdfReader

SECTION_TITLES = [
    "Career Preference",
    "Education",
    "Specific details 1",
    "Achievements and Learning",
    "Challenges",
    "Leadership Experience",
    "About the Project",
    "About Product Development",
    "About Japanese Companies",
    "Research and Development",
    "About interdisciplinary communities of interest and research and development",
    "Interest Areas",
    "Most interested point",
    "Things you want to learn",
    "About career paths",
    "Interesting Roles",
    "3 major priority factors",
]

def extract_text(path):
    reader = PdfReader(path)
    full_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text.extend(line.strip() for line in text.splitlines())
    return full_text

def split_sections(lines):
    sections = {}       # ← here we define the container for each section
    current = None      # ← this tracks which section we’re filling

    # Determine which predefined titles actually appear
    present = [t for t in SECTION_TITLES if t in lines]

    for line in lines:
        if line in present:
            current = line
            sections[current] = []      # ← here we “define” a new section entry
            continue

        if current:
            if line.isupper():
                # Treat uppercase lines as sub‑headings
                sections[current].append({
                    "subheading": line,
                    "content": []
                })
                continue

            last = sections[current][-1] if sections[current] else None
            if isinstance(last, dict):
                last["content"].append(line)
            else:
                sections[current].append(line)

    # Convert lists of lines into joined strings where no sub‑heading dicts exist
    for key, items in sections.items():
        normalized = []
        for item in items:
            if isinstance(item, dict):
                # keep dicts as‑is
                normalized.append(item)
            else:
                normalized.append(item)
        sections[key] = normalized

    return sections


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="input PDF path")
    p.add_argument("--output", required=True, help="output JSON path")
    args = p.parse_args()

    lines = extract_text(args.input)
    data = split_sections(lines)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4,
            separators=(", ", ": ")
        )

if __name__ == "__main__":
    main()
