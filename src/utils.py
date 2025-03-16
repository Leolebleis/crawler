from urllib.parse import urlparse


def normalize_url(url: str) -> str:
    """
    Normalize a URL to avoid processing duplicates.
    :param url: The URL to normalize.
    :return: The normalized URL.
    """
    parsed_url = urlparse(url)
    # Normalize scheme and netloc (hostname + port)
    scheme = parsed_url.scheme.lower()
    netloc = parsed_url.netloc.lower()
    # Remove fragments and normalize path
    normalized_url = parsed_url._replace(
        scheme=scheme, netloc=netloc, fragment="", path=parsed_url.path.rstrip("/")
    )
    return normalized_url.geturl()
