import argparse
import asyncio
import logging
import time
from urllib.parse import urlparse

from service.parser import parse
from src.client.http_client import Client
from src.service.frontier import Frontier
from src.service.reporter import Reporter

logger = logging.getLogger(__name__)

async def worker(allowed_netloc: str, reporter: Reporter, frontier: Frontier, max_depth: int,
                 depth_reached: asyncio.Event) -> None:
    client = Client(allowed_netloc)
    try:
        while not depth_reached.is_set():
            url = await frontier.get_next_url()
            if url is None:
                await asyncio.sleep(0.1)  # Prevent tight loop if queue is empty
                continue

            final_url, content = await client.fetch(url)
            if content:
                links = parse(final_url, content)
                reporter.record(final_url, links)

                # Check depth before adding new links
                if len(reporter.results) >= max_depth:
                    depth_reached.set()
                    break

                for link in links:
                    if len(reporter.results) < max_depth:
                        await frontier.add_url(link)
                    else:
                        break
    finally:
        await client.close()

async def main(start_url: str, num_workers: int, depth: int) -> None:
    logger.info(f"Starting the crawler with {num_workers} workers...")
    start_time = time.perf_counter()

    base_netloc = urlparse(start_url).netloc
    frontier = Frontier(base_netloc)
    await frontier.add_url(start_url)
    reporter = Reporter()

    # Create a shared event to signal when depth is reached
    depth_reached = asyncio.Event()

    # Worker tasks
    tasks = [
        asyncio.create_task(
            worker(base_netloc, reporter, frontier, depth, depth_reached)
        )
        for _ in range(num_workers)
    ]

    await asyncio.gather(*tasks)

    end_time = time.perf_counter()
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