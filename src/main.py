import argparse
import asyncio
import logging
import time
from urllib.parse import urlparse

from src.client.http_client import Client
from src.service.crawler import Crawler
from src.service.frontier import Frontier
from src.service.reporter import Reporter

logger = logging.getLogger(__name__)

async def worker(start_url: str, depth: int, allowed_netloc: str, reporter: Reporter, frontier: Frontier) -> None:
    client = Client(allowed_netloc)

    crawler = Crawler(depth, frontier, client, reporter)
    await crawler.run()
    await client.close()

async def main(start_url: str, num_workers: int, depth: int) -> None:
    logger.info(f"Starting the crawler with {num_workers} workers...")
    start_time = time.time()

    base_netloc = urlparse(start_url).netloc

    frontier = Frontier(base_netloc)
    await frontier.add_url(start_url)
    reporter = Reporter()

    tasks = [worker(start_url, depth, base_netloc, reporter, frontier) for _ in range(num_workers)]
    await asyncio.gather(*tasks)

    end_time = time.time()
    duration = end_time - start_time

    reporter.output()

    logger.debug(f"Crawling completed in {duration:.2f} seconds")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="A simple web crawler.")
    parser.add_argument(
        "--start-url",
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
        "--depth",
        type=int,
        default=10,
        help="The maximum depth to crawl. Defaults to 10.",
    )

    args = parser.parse_args()

    # Run the crawler
    asyncio.run(main(args.start_url, args.workers, args.depth))