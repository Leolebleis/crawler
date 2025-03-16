import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.service.crawler import Crawler


@pytest.fixture
def mock_frontier():
    frontier = MagicMock()
    frontier.get_next_url = AsyncMock()
    frontier.add_url = AsyncMock()
    return frontier


@pytest.fixture
def mock_client():
    client = MagicMock()
    client.fetch = AsyncMock()
    return client


@pytest.fixture
def mock_reporter():
    reporter = MagicMock()
    reporter.results = {}
    reporter.record = MagicMock()
    return reporter


@pytest.fixture
def max_pages_reached():
    return asyncio.Event()


@pytest.mark.asyncio
async def test_crawler_stops_at_max_pages(
    mock_frontier, mock_client, mock_reporter, max_pages_reached
):
    # Mock behavior
    urls = [f"https://example.com/page{i}" for i in range(5)]
    mock_frontier.get_next_url.side_effect = urls

    content = f"""
    <html>
        {"".join(f'<a href="{url}"></a>' for url in urls)}
    </html>
    """
    mock_client.fetch.return_value = ("https://example.com", content)

    mock_frontier.get_next_url.side_effect = urls

    mock_reporter.record.side_effect = lambda url, links: mock_reporter.results.update(
        {url: links}
    )

    max_pages = 1
    crawler = Crawler(
        frontier=mock_frontier,
        client=mock_client,
        reporter=mock_reporter,
        max_pages_reached=max_pages_reached,
        max_pages=max_pages,
    )

    # Run the crawler
    await crawler.run()

    # Check the results
    assert mock_reporter.record.call_count == max_pages


def test_crawler_stops_when_not_enough_pages() -> None: ...
