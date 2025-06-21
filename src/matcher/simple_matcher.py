from typing import List, Dict
import re


def normalize_token(token: str) -> str:
    return token.strip().lower()


def tokenize_text(text: str) -> List[str]:
    # Simple split on non-alphanumeric for English; for more languages, extend later
    tokens = re.split(r"[^0-9a-zA-Z]+", text.lower())
    return [t for t in tokens if t]


def match_skills_to_jobs(skills: List[str], jobs: List[Dict[str, str]], top_n: int =10) -> List[Dict[str, object]]:
    """Compute simple keyword-overlap matching: count occurrences of skill tokens in job title+description."""
    norm_skills = [normalize_token(s) for s in skills]
    results = []
    for job in jobs:
        text = f"{job.get('title','')} {job.get('description','')}"
        tokens = tokenize_text(text)
        score = 0
        matched = []
        for sk in norm_skills:
            if not sk:
                continue
            # match whole token or substring? Here substring in full text may catch e.g. 'java' in 'javascript'; for Phase1, accept but note limitation
            if sk in text.lower():
                score += 1
                matched.append(sk)
        results.append({"job": job, "score": score, "matched_skills": matched})
    # sort by score desc
    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
    # filter zero-score or include per design; here include only score>0
    filtered = [r for r in sorted_results if r["score"] > 0]
    return filtered[:top_n]