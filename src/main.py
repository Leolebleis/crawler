import argparse
import asyncio
import logging
import time
from urllib.parse import urlparse

from service.crawler import Crawler
from src.client.http_client import Client
from src.service.frontier import Frontier
from src.service.reporter import Reporter

_DEFAULT_LOG_LEVEL = logging.INFO

_logger = logging.getLogger(__name__)


async def main(start_url: str, num_workers: int, max_pages: int) -> None:
    _logger.info(f"Starting the crawler with {num_workers} workers...")
    start_time = time.perf_counter()

    # Initialize the components
    base_netloc = urlparse(start_url).netloc
    frontier = Frontier(base_netloc)
    # We add the start URL to the frontier to kick off the crawling process.
    await frontier.add_url(start_url)
    reporter = Reporter()
    client = Client(base_netloc)

    # Create a shared event to signal when max number of pages is reached.
    # This is a coroutine-safe way to warn all workers to stop crawling when the limit is reached.
    max_pages_reached = asyncio.Event()

    # We create the workers, each of which will run an instance of the Crawler class.
    tasks = [
        asyncio.create_task(
            Crawler(frontier, client, reporter, max_pages_reached, max_pages).run()
        )
        for _ in range(num_workers)
    ]

    await asyncio.gather(*tasks)

    end_time = time.perf_counter()
    duration = end_time - start_time

    # Log the results
    reporter.output()
    _logger.info(f"Crawled {len(reporter.results)} pages in {duration:.2f} seconds")

    # We close the client after all tasks are done to ensure all connections are closed properly.
    await client.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=_DEFAULT_LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="A simple web crawler.")
    parser.add_argument(
        "--start-url",
        type=str,
        default="https://monzo.com",
        help="The URL to start crawling from. Defaults to https://monzo.com.",
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=5,
        help="The number of concurrent workers. Defaults to 5.",
    )

    parser.add_argument(
        "--max-pages",
        type=int,
        default=10,
        help="The maximum pages to crawl. Defaults to 10.",
    )

    args = parser.parse_args()

    # Run the crawler
    asyncio.run(main(args.start_url, args.workers, args.max_pages))
