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

    def __init__(self, depth: int, frontier: Frontier, client: Client, reporter: Reporter) -> None:
        self._frontier = frontier
        self._client = client
        self._reporter = reporter
        self._depth = depth

    async def run(self) -> None:
        """
        Run the crawler to fetch and parse URLs.
        :return: None
        """
        count = 0
        while self._frontier.has_next() and count < self._depth:
            url = await self._frontier.get_next_url()
            if not url:
                break
            final_url, content = await self._client.fetch(url)
            if content:
                links = parse(final_url, content)
                self._reporter.record(final_url, links)
                for link in links:
                    await self._frontier.add_url(link)
            count += 1
