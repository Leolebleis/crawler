import logging
from typing import Optional

import requests
from urllib.parse import urlparse
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

class Fetcher:
    def __init__(self, allowed_netloc: str) -> None:
        """
        Initialize the Fetcher.
        :param allowed_netloc: The netloc of the domain to crawl.
        """
        self.allowed_netloc = allowed_netloc
        self.session = requests.Session()  # Reuse connections for efficiency
        # TODO: use aiohttp for async requests
        # TODO: respect robots.txt

    async def fetch(self, url: str) -> tuple[Optional[str], Optional[str]]:
        """
        Fetch the content of a URL.
        :param url: The URL to fetch.
        :return: A tuple of (final_url, content) if successful, or (None, None) on failure.
        """
        try:
            # Send a GET request with a timeout
            response = self.session.get(url, timeout=10, headers={"User-Agent": "WebCrawler/1.0"})
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)

            # Ensure the final URL is within the allowed domain
            final_url = response.url
            if urlparse(final_url).netloc != self.allowed_netloc:
                logger.debug(f"Skipping external URL: {final_url}")
                return None, None

            # Ensure the response is HTML
            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                logger.debug(f"Skipping non-HTML content: {final_url} ({content_type})")
                return None, None

            return final_url, response.text

        except RequestException as e:
            logger.debug(f"Failed to fetch {url}: {e}")
            return None, None