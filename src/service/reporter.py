from typing import Dict, Set

from aiologger import Logger

logger = Logger.with_default_handlers()

class Reporter:
    def __init__(self):
        """
        Initialize the Reporter.
        """
        self.results: Dict[str, Set[str]] = {}  # Maps URLs to their discovered links

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
            logger.info(f"URL: {url}")
            logger.info("Links:")
            for link in links:
                logger.info(f"  - {link}")
            logger.info("")  # Add a blank line between entries