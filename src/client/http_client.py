import asyncio
import logging
from typing import Optional
from urllib.parse import urlparse

import aiohttp

logger = logging.getLogger(__name__)


class Client:
    """
    Client is responsible for making HTTP requests to fetch the content of URLs.
    It uses aiohttp for asynchronous requests and handles redirects and content type checks.
    It ensures that only HTML content from the allowed domain is processed.
    """
    def __init__(self, allowed_netloc: str) -> None:
        """
        Initialize the Client.
        :param allowed_netloc: The netloc of the domain to crawl.
        """
        self._allowed_netloc = allowed_netloc
        self._session: Optional[aiohttp.ClientSession] = None

    async def fetch(self, url: str) -> tuple[Optional[str], Optional[str]]:
        """
        Fetch the content of a URL asynchronously.
        :param url: The URL to fetch.
        :return: A tuple containing the URL (after redirects) and content, or None if an error occurred.
        """
        if not self._session:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10),
                headers={"User-Agent": "WebCrawler/1.0"},
            )

        try:
            logger.debug(f"Fetching URL: {url}")
            async with self._session.get(url) as response:
                response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)

                # Ensure the final URL is within the allowed domain after redirects
                final_url = str(response.url)
                if urlparse(final_url).netloc != self._allowed_netloc:
                    logger.debug(f"Skipping external URL: {final_url}")
                    return None, None

                # Ensure the response is HTML
                content_type = response.headers.get("Content-Type", "")
                if "text/html" not in content_type:
                    logger.debug(
                        f"Skipping non-HTML content: {final_url} ({content_type})"
                    )
                    return None, None

                content = await response.text()
                return final_url, content

        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logger.debug(f"Failed to fetch {url}: {e}")
            return None, None

    async def close(self) -> None:
        """
        Close the aiohttp session.
        """
        if self._session:
            await self._session.close()
