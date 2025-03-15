from urllib.parse import urlparse, urlunparse

def normalize_url(url):
    """
    Normalize a URL to avoid processing duplicates.
    :param url: The URL to normalize.
    :return: The normalized URL.
    """
    parsed_url = urlparse(url)
    # Normalize scheme and netloc (hostname + port)
    scheme = parsed_url.scheme.lower()
    netloc = parsed_url.netloc.lower()
    # Remove default ports (e.g., :80 for HTTP, :443 for HTTPS)
    if ":" in netloc:
        host, port = netloc.split(":", 1)
        if (scheme == "http" and port == "80") or (scheme == "https" and port == "443"):
            netloc = host
    # Remove fragments and normalize path
    normalized_url = parsed_url._replace(
        scheme=scheme,
        netloc=netloc,
        fragment="",
        path=parsed_url.path.rstrip("/")
    )
    return normalized_url.geturl()