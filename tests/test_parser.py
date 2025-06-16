import os
import sys
import json
import subprocess

dir_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, dir_root)

from parser_module.parse_skill_sheet import extract_text, split_sections

def test_split_sections_basic():
    # Sample lines with section titles and a subheading
    lines = [
        "Education",
        "2024 Indian Institute of Technology, Delhi",
        "CAREER SUMMARY",
        "Experienced engineer in robotics",
        "Leadership Experience",
        "Led team of 5 in AGV project",
    ]
    sections = split_sections(lines)
    assert "Education" in sections
    assert "Leadership Experience" in sections
    # Subheading should be detected as dict entry
    edu_items = sections["Education"]
    assert any(isinstance(item, dict) and item["subheading"] == "CAREER SUMMARY" for item in edu_items)

def test_sections_extracted_from_pdf(tmp_path, monkeypatch):
    sample_lines = [
        "Career Preference", "Software Developer in Japan",
        "Challenges", "Integrating LiDAR data in ROS2",
    ]

    monkeypatch.setattr(
        "parser_module.parse_skill_sheet.extract_text",
        lambda path: sample_lines
    )

    from parser_module.parse_skill_sheet import split_sections

    data = split_sections(sample_lines)

    assert isinstance(data, dict)
    assert data.get("Career Preference") == "Software Developer in Japan"
    assert data.get("Challenges") == "Integrating LiDAR data in ROS2"



if __name__ == "__main__":
    import pytest
    exit_code = pytest.main([os.path.basename(__file__)])
    sys.exit(exit_code)
