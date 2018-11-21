import requests
from urllib.parse import urlparse
import posixpath

BASE_URL = "https://api.chess.com/pub/"


def request_json(endpoint: str) -> dict:
    """Call the given endpoint and return the response as a dict.

    In case of error, raises an unhelpful exception for now."""
    r = requests.get(BASE_URL + endpoint)
    # For illustration only, rely on logging in the future
    print("Getting: " + endpoint)
    if r.status_code is not 200:
        raise Exception()
    d = r.json()
    assert type(d) is dict
    return d


def key_from_url(url):
    """Retrieve the last component of an URL."""
    path = urlparse(url).path
    _, key = posixpath.split(path)
    return key
