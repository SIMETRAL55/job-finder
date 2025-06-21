import os
import pytest
from src.parser.pdf_parser import extract_text_lines

def test_extract_text_lines_nonempty():
    sample = os.path.join(os.path.dirname(__file__), "..", "src", "data", "samples", "Wasim_Shaikh_Translated_Skill_Sheet.pdf")
    # Allow adjusting path: user should place sample under src/data/samples/
    if not os.path.isfile(sample):
        pytest.skip("Sample PDF not found for test.")
    lines = extract_text_lines(sample)
    assert isinstance(lines, list)
    assert len(lines) > 0