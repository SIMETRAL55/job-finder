import os
from src.scraper.job_scraper import scrape_jobs

def test_scrape_mock_html(tmp_path):
    # Create a small mock HTML
    html = '''<div class="job-card"><h2 class="title">Test Role</h2><p class="desc">Skill A, Skill B</p><a href="https://example.com">Apply</a></div>'''
    file = tmp_path / "mock.html"
    file.write_text(html, encoding="utf-8")
    config = {"type": "mock", "path": str(file)}
    jobs = scrape_jobs(config)
    assert isinstance(jobs, list)
    assert len(jobs) == 1
    assert jobs[0]["title"] == "Test Role"
    assert "Skill A" in jobs[0]["description"]