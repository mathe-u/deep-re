"""Extract"""

import re

def data_treat(text: str) -> str:
    """treat text data."""
    new_text = ""
    if text:
        new_text = text.replace("\xa0", " ")
        new_text = text.replace("…", "")
    return new_text


def extract_year(text):
    """Extract year of pub."""
    new_text = data_treat(text)
    pattern = r"\b\d{4}\b"
    res = re.search(pattern=pattern, string=new_text)

    if res:
        return res.group(0)

    return ""

def extract_about(text: str) -> str:
    """Extract authors, jornal, etc... of pub."""
    new_text = data_treat(text)
    res = re.sub(pattern=extract_year(text=new_text), repl="", string=new_text)

    if res:
        return res

    return ""
