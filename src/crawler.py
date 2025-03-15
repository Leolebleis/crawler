from urllib.parse import urlparse, urlunparse

from src.fetcher import Fetcher
from src.frontier import Frontier
from src.parser import Parser
from src.reporter import Reporter
from src.utils import normalize_url


class Crawler:
    """
    Crawler is the main class that orchestrates the crawling process. It uses
    a Frontier to manage the URLs to crawl, a Fetcher to fetch the content of
    the URLs, a Parser to extract links from the content, and a Reporter to
    record the URLs and links and eventually output them.
    """
    def __init__(self,
                 start_url: str,

                 ) -> None:
        self.start_url = start_url
        self.allowed_netloc = urlparse(normalize_url(start_url)).netloc
        self.frontier = Frontier(self.allowed_netloc)
        self.fetcher = Fetcher(self.allowed_netloc)
        self.parser = Parser()
        self.reporter = Reporter()
        self.frontier.add_url(self.start_url)

    async def run(self) -> None:
        """
        Run the crawler to fetch and parse URLs.
        :return: None
        """
        while self.frontier.has_next():
            url = self.frontier.get_next_url()
            if not url:
                break

            final_url, content = self.fetcher.fetch(url)
            if content:
                links = self.parser.parse(final_url, content)
                self.reporter.record(final_url, links)
                for link in links:
                    self.frontier.add_url(link)
        self.reporter.output()

