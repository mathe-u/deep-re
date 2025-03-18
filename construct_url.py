"""Consturct url"""
# import random

def construct_url(
        baseurl,
        patents=True,
        citations=True,
        year_start=None,
        start_index=0,
    ):
    """Construct urls"""
    url = baseurl
    patents = "as_sdt=2007" if patents else "as_sdt=0,5"
    citations = f"as_vis={1 - int(citations)}"
    yr_lo = f"as_ylo={year_start}" if year_start is not None else ""
    start = f"start={start_index}" if start_index > 0 else ""
    pieces = [patents, citations, yr_lo, start]
    # random.shuffle(pieces)
    random_url = "&".join(pieces)
    return url + "&" + random_url
