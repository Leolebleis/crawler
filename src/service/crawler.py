import asyncio
import logging

from src.client.http_client import Client
from src.service.frontier import Frontier
from src.service.parser import parse
from src.service.reporter import Reporter

_logger = logging.getLogger(__name__)


class Crawler:
    """
    Crawler is the main class that orchestrates the crawling process. It uses
    a Frontier to manage the URLs to crawl, a Client to fetch the content of
    the URLs, a Parser to extract links from the content, and a Reporter to
    record the URLs and links and eventually output them.
    """

    def __init__(
            self,
            worker_id: int,
            frontier: Frontier,
            client: Client,
            reporter: Reporter,
            max_pages_reached: asyncio.Event,
            max_pages: int,
    ) -> None:
        self._id = worker_id
        self._frontier = frontier
        self._client = client
        self._reporter = reporter
        self._max_pages = max_pages
        self._max_pages_reached = max_pages_reached

    async def run(self) -> None:
        """
        Run the crawler to fetch and parse URLs.
        :return: None
        """
        while not self._max_pages_reached.is_set():
            url = await self._frontier.get_next_url()
            if not url:
                _logger.debug(f"Queue is empty. Stopping the crawler worker with id={self._id}.")
                break

            if self._is_max_pages_reached():
                self._max_pages_reached.set()
                _logger.debug(f"Max number of pages reached. Stopping the crawler worker with id={self._id}.")
                break

            final_url, content = await self._client.fetch(url)
            if not content:
                _logger.error(f"Failed to fetch content from {url}.")
                continue
            links = parse(final_url, content)

            self._reporter.record(url, links)

            for link in links:
                await self._frontier.add_url(link)

        _logger.info(f"Stopping the crawler worker with id={self._id}.")

    def _is_max_pages_reached(self) -> bool:
        """
        Check if the maximum number of pages has been reached.
        :return: True if max pages reached, False otherwise.
        """
        return len(self._reporter.results) >= self._max_pages
