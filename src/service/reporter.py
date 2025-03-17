import logging

_logger = logging.getLogger(__name__)


class Reporter:
    """
    Reporter is responsible for recording the URLs and their discovered links.
    It maintains a dictionary mapping URLs to sets of links.
    The output method prints the results to the console.
    """
    def __init__(self, max_size: int) -> None:
        """
        Initialize the Reporter.
        """
        self._max_size = max_size
        self.results: dict[str, set[str]] = {}  # Maps URLs to their discovered links

    def record(self, url: str, links: set[str]) -> None:
        """
        Record the links found on a page.
        :param url: The URL of the page.
        :param links: A set of links found on the page.
        """
        if len(self.results) >= self._max_size:
            _logger.debug("Tried to record despite max size reached.")
            return
        self.results[url] = links

    def output(self):
        """
        Output the results to the console using logger.info.
        """
        for url, links in self.results.items():
            _logger.info(f"URL: {url}")
            _logger.info("Links:")
            for link in links:
                _logger.info(f"  - {link}")
            _logger.info("")  # Add a blank line between entries
