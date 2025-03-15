from queue import Queue
from typing import Optional
from urllib.parse import urlparse

from src.utils import normalize_url


class Frontier:
    """
    Frontier is a queue of URLs to crawl. It keeps track of the URLs that have
    been added and those that have been visited.
    """
    def __init__(self, allowed_netloc: str) -> None:
        self.allowed_netloc  = allowed_netloc
        self.visited = set() # URLs that have been visited
        self.queue = Queue() # This is thread safe and can be used with asyncio

    def add_url(self, url: str) -> None:
        """
        Add a URL to the frontier if it is valid and has not been visited.
        :param url: The URL to add.
        :return: None
        """
        normalized_url = normalize_url(url)
        if self._is_valid_url(normalized_url) and normalized_url not in self.visited:
            self.visited.add(normalized_url)
            self.queue.put(normalized_url)

    def get_next_url(self) -> Optional[str]:
        """
        Get the next URL from the frontier.
        :return: The next URL to crawl, or None if the frontier is empty.
        """
        if not self.queue.empty():
            return self.queue.get()
        return None

    def _is_valid_url(self, url):
        """
        Check if a URL is within the allowed domain.
        :param url: The URL to check.
        :return: True if the URL is valid, False otherwise.
        """
        parsed_url = urlparse(url)
        return parsed_url.netloc == self.allowed_netloc

    def has_next(self):
        """
        Check if there are more URLs to crawl.
        :return: True if the queue is not empty, False otherwise.
        """
        return not self.queue.empty()