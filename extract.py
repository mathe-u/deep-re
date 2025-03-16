"""Extract"""

import re

def extract_year(text):
    """Extract year of pub."""
    pattern = r"\b\d{4}\b"
    res = re.search(pattern=pattern, string=text)

    if res:
        return res.group(0)

    return None

def extract_authors(text):
    """Extract authors of pub."""
    pattern = r"(.+?) - "
    res = re.search(pattern=pattern, string=text)

    if res:
        return res.group(1)

    return None

def extract_journal(text, is_citation):
    """Extract journal of pub."""
    text = text.strip()
    if is_citation:
        pattern = r"- (.+?)"
    else:
        pattern = r"- (.+?),"
    res = re.search(pattern=pattern, string=text)

    if res:
        return res.group(1)
    return None
