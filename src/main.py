import argparse
import json
import os
import yaml
from src.utils.file_utils import detect_file_type
from src.parser.pdf_parser import extract_text_lines
from src.extractor.field_extractor import extract_fields_from_text, extract_fields_from_xlsx


def main():
    parser = argparse.ArgumentParser(description="Prototype: parse skill sheet and store extracted fields as JSON (no scraping).")
    parser.add_argument("--input-file", required=True, help="Path to PDF or XLSX skill sheet")
    parser.add_argument("--config", default="config/config.yaml", help="Path to config YAML")
    parser.add_argument("--output", default="src/data/outputs/result.json", help="Path for output JSON")
    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print(f"Input file not found: {args.input_file}")
        return
    if not os.path.isfile(args.config):
        print(f"Config file not found: {args.config}")
        return
    with open(args.config, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    try:
        ftype = detect_file_type(args.input_file)
    except ValueError as e:
        print(str(e))
        return
    if ftype == "pdf":
        lines = extract_text_lines(args.input_file)
        fields = extract_fields_from_text(lines, config)
    else:
        fields = extract_fields_from_xlsx(args.input_file, config)
    print("Extracted sections:", list(fields.keys()))
    # Prepare a flattened list of lines under all sections
    skills = []
    for sec, content in fields.items():
        for item in content:
            if isinstance(item, dict):
                skills.extend(item.get("content", []))
            else:
                skills.append(item)
    skills = [s for s in {s.strip() for s in skills if s.strip()}]
    print(f"Total extracted lines: {len(skills)}")
    # Prepare output JSON with extracted fields and flattened lines
    output_data = {"fields": fields, "lines": skills}
    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as outf:
        json.dump(output_data, outf, ensure_ascii=False, indent=4)
    print(f"Extracted information written to {args.output}")

if __name__ == "__main__":
    main()