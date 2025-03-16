from typing import Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup  # HTML parsing library

from src.utils import normalize_url

ALLOWED_SCHEMES = ("http", "https", "/")


def parse(base_url: str, html: str) -> set[str]:
    """
    Parse the HTML content and extract all valid links.
    :param base_url: The URL of the page being parsed (used to resolve relative URLs).
    :param html: The HTML content of the page.
    :return: A set of normalized, absolute URLs.
    """
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        absolute_url = _make_absolute_url(base_url, href)
        if absolute_url:
            links.add(absolute_url)

    return links


def _make_absolute_url(base_url: str, href: str) -> Optional[str]:
    """
    Convert a relative URL to an absolute URL and normalize it.
    :param base_url: The base URL of the page.
    :param href: The href attribute from an anchor tag.
    :return: The normalized absolute URL, or None if the URL is invalid.
    """
    # Skip unwanted URLs (e.g., mailto, javascript)
    if not href or not href.startswith(ALLOWED_SCHEMES):
        return None

    # Join the base URL and the href to form an absolute URL
    absolute_url = urljoin(base_url, href)

    # Normalize the URL
    normalized_url = normalize_url(absolute_url)

    return normalized_url
