from src.matcher.simple_matcher import match_skills_to_jobs

def test_match_skills_to_jobs():
    skills = ["Python", "React"]
    jobs = [
        {"title": "Backend Developer", "description": "Python, Django, REST", "url": ""},
        {"title": "Frontend Engineer", "description": "JavaScript, React, HTML", "url": ""},
        {"title": "Manager", "description": "Management skills", "url": ""}
    ]
    matches = match_skills_to_jobs(skills, jobs, top_n=5)
    # Expect two matches: first two
    titles = [m["job"]["title"] for m in matches]
    assert "Backend Developer" in titles
    assert "Frontend Engineer" in titles
    assert all(m["score"] > 0 for m in matches)