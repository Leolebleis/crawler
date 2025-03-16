import logging

_logger = logging.getLogger(__name__)


class Reporter:
    def __init__(self):
        """
        Initialize the Reporter.
        """
        self.results: dict[str, set[str]] = {}  # Maps URLs to their discovered links

    def record(self, url, links):
        """
        Record the links found on a page.
        :param url: The URL of the page.
        :param links: A set of links found on the page.
        """
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
