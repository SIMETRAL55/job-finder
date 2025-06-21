import os
from typing import List, Dict
from bs4 import BeautifulSoup
import requests


def scrape_jobs(config_entry: Dict[str, str]) -> List[Dict[str, str]]:
    """Scrape jobs either from mock HTML file or real URL based on config_entry."""
    html = None
    if config_entry.get("type") == "mock":
        path = config_entry.get("path")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Mock HTML file not found: {path}")
        with open(path, encoding="utf-8") as f:
            html = f.read()
    else:
        url = config_entry.get("url")
        if not url:
            raise ValueError("No URL provided for scraper target.")
        headers = {"User-Agent": "prototype-bot/1.0"}
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        html = resp.text
    soup = BeautifulSoup(html, "html.parser")
    jobs = []
    # Default selectors for mock: .job-card, .title, .desc, <a>
    list_selector = config_entry.get("list_selector", ".job-card")
    title_selector = config_entry.get("title_selector", ".title")
    desc_selector = config_entry.get("desc_selector", ".desc")
    for card in soup.select(list_selector):
        title_tag = card.select_one(title_selector)
        desc_tag = card.select_one(desc_selector)
        link_tag = card.select_one("a")
        title = title_tag.get_text(strip=True) if title_tag else ""
        desc = desc_tag.get_text(strip=True) if desc_tag else ""
        url = link_tag["href"] if link_tag and link_tag.has_attr("href") else ""
        jobs.append({"title": title, "description": desc, "url": url})
    return jobs