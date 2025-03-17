import asyncio
import logging
from typing import Optional
from urllib.parse import urlparse

from src.utils import normalize_url

_logger = logging.getLogger(__name__)


class Frontier:
    """
    Frontier is responsible for managing the URLs to be crawled.
    It maintains a queue of URLs and ensures that only valid URLs are added.
    It also keeps track of visited URLs to avoid duplicates.
    """
    def __init__(self, allowed_netloc: str, timeout: int = 10) -> None:
        self._allowed_netloc = allowed_netloc
        self._visited = set()
        self._queue = asyncio.Queue()
        self._timeout = timeout

    async def add_url(self, url: str) -> None:
        normalized_url = normalize_url(url)
        if self._is_valid_url(normalized_url) and normalized_url not in self._visited:
            self._visited.add(normalized_url)
            await self._queue.put(normalized_url)

    async def get_next_url(self) -> Optional[str]:
        try:
            return await asyncio.wait_for(self._queue.get(), timeout=self._timeout)
        except asyncio.TimeoutError:
            _logger.error("Queue is empty")
            return None

    def _is_valid_url(self, url: str) -> bool:
        parsed_url = urlparse(url)
        return parsed_url.netloc == self._allowed_netloc

    def has_next(self) -> bool:
        return not self._queue.empty()
