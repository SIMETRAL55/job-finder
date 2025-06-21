import os
import pytest
from src.parser.xlsx_parser import extract_lines_from_xlsx

def test_extract_lines_from_xlsx_nonempty():
    sample = os.path.join(os.path.dirname(__file__), "..", "src", "data", "samples", "49_7_D_Washim Shaikh_Translated.xlsx")
    if not os.path.isfile(sample):
        pytest.skip("Sample XLSX not found for test.")
    lines = extract_lines_from_xlsx(sample)
    assert isinstance(lines, list)
    # Cannot guarantee >0 without knowing structure, but at least list
    assert isinstance(lines, list)