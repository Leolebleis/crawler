import asyncio
from typing import Optional
from urllib.parse import urlparse

from src.utils import normalize_url


class Frontier:
    def __init__(self, allowed_netloc: str) -> None:
        self.allowed_netloc = allowed_netloc
        self.visited = set()
        self.queue = asyncio.Queue()

    async def add_url(self, url: str) -> None:
        normalized_url = normalize_url(url)
        if self._is_valid_url(normalized_url) and normalized_url not in self.visited:
            self.visited.add(normalized_url)
            await self.queue.put(normalized_url)

    async def get_next_url(self) -> Optional[str]:
        if not self.queue.empty():
            return await self.queue.get()
        return None

    def _is_valid_url(self, url: str) -> bool:
        parsed_url = urlparse(url)
        return parsed_url.netloc == self.allowed_netloc

    def has_next(self) -> bool:
        return not self.queue.empty()
