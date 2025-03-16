import requests
from construct_url import construct_url

def search_pubs(query, patents=True, citations=True, year_start=None, start_index=0):
    pubsearch = f"/scholar?hl=pt-BR&q={requests.utils.quote(query)}"
    url = construct_url(
        pubsearch,
        patents=patents,
        citations=citations,
        year_start=year_start,
        start_index=start_index,
    )
    return url
