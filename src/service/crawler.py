import asyncio
import logging

from src.client.http_client import Client
from src.service.frontier import Frontier
from src.service.parser import parse
from src.service.reporter import Reporter

logger = logging.getLogger(__name__)


class Crawler:
    """
    Crawler is the main class that orchestrates the crawling process. It uses
    a Frontier to manage the URLs to crawl, a Client to fetch the content of
    the URLs, a Parser to extract links from the content, and a Reporter to
    record the URLs and links and eventually output them.
    """

    def __init__(
        self,
        frontier: Frontier,
        client: Client,
        reporter: Reporter,
        max_pages_reached: asyncio.Event,
        max_pages: int,
    ) -> None:
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
            if url is None:
                await asyncio.sleep(0.1)  # TODO: this is really bad
                continue

            final_url, content = await self._client.fetch(url)
            if content:
                links = parse(final_url, content)
                # Check number of pages before adding new links
                if len(self._reporter.results) >= self._max_pages:
                    self._max_pages_reached.set()
                    break

                self._reporter.record(final_url, links)

                for link in links:
                    if len(self._reporter.results) < self._max_pages:
                        await self._frontier.add_url(link)
                    else:
                        break
