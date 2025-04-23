import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.service.crawler import Crawler


class TestException(Exception):
    __test__ = False
    pass


@pytest.fixture
def mock_frontier() -> MagicMock:
    frontier = MagicMock()
    frontier.get_next_url = AsyncMock()
    frontier.add_url = AsyncMock()
    return frontier


@pytest.fixture
def mock_client() -> MagicMock:
    client = MagicMock()
    client.fetch = AsyncMock()
    return client


@pytest.fixture
def mock_reporter() -> MagicMock:
    reporter = MagicMock()
    reporter.results = {}
    reporter.record = MagicMock()
    return reporter


@pytest.fixture
def max_pages_reached() -> asyncio.Event:
    return asyncio.Event()


async def test_crawler_runs_successfully(
        mock_frontier: MagicMock, mock_client: MagicMock, mock_reporter: MagicMock, max_pages_reached: asyncio.Event
) -> None:
    # Mock behavior
    mock_frontier.get_next_url.side_effect = [
        "https://example.com/page1",
        "https://example.com/page2",
        None,  # Simulate empty queue
    ]
    mock_client.fetch.side_effect = [
        ("https://example.com/page1", """<html><a href="https://example.com/page3">Link</a></html>"""),
        ("https://example.com/page2", """<html><a href="https://example.com/page4">Link</a></html>"""),
    ]
    mock_reporter.results = {}  # Start with no results

    crawler = Crawler(
        worker_id=1,
        frontier=mock_frontier,
        client=mock_client,
        reporter=mock_reporter,
        max_pages_reached=max_pages_reached,
        max_pages=5,
    )

    # Run the crawler
    await crawler.run()

    # Assertions
    assert not max_pages_reached.is_set()
    assert mock_frontier.get_next_url.call_count == 3  # Two pages + None
    assert mock_client.fetch.call_count == 2
    assert mock_reporter.record.call_count == 2
    assert mock_frontier.add_url.call_count == 2


async def test_crawler_stops_at_max_pages(
        mock_frontier: MagicMock, mock_client: MagicMock, mock_reporter: MagicMock, max_pages_reached: asyncio.Event
) -> None:
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
        worker_id=1,
        frontier=mock_frontier,
        client=mock_client,
        reporter=mock_reporter,
        max_pages_reached=max_pages_reached,
        max_pages=max_pages,
    )

    # Run the crawler
    await crawler.run()

    # Check the reporter only has the right number of pages
    assert mock_reporter.record.call_count == max_pages
    assert len(mock_reporter.results) == max_pages


async def test_crawler_processes_until_queue_empty(
        mock_frontier: MagicMock, mock_client: MagicMock, mock_reporter: MagicMock, max_pages_reached: asyncio.Event
) -> None:
    # Mock behavior
    mock_frontier.get_next_url.side_effect = [
        "https://example.com/page1",
        "https://example.com/page2",
        None,  # Simulate empty queue
    ]
    mock_client.fetch.return_value = ("https://example.com/page1", "<html>...</html>")
    mock_reporter.results = {}  # Start with no results

    crawler = Crawler(
        worker_id=1,
        frontier=mock_frontier,
        client=mock_client,
        reporter=mock_reporter,
        max_pages_reached=max_pages_reached,
        max_pages=5,
    )
    # Run crawler
    await crawler.run()

    # Assertions
    assert not max_pages_reached.is_set()
    assert mock_frontier.get_next_url.call_count == 3
    mock_client.fetch.assert_called()
    mock_reporter.record.assert_called()


async def test_crawler_handles_unexpected_fetch_errors(
        mock_frontier: MagicMock, mock_client: MagicMock, mock_reporter: MagicMock, max_pages_reached: asyncio.Event
) -> None:
    # Mock behavior
    mock_frontier.get_next_url.return_value = "https://example.com/page1"
    mock_client.fetch.side_effect = TestException("Fetch failed")  # Simulate fetch error
    mock_reporter.results = {}  # Start with no results

    with pytest.raises(TestException):
        # Run crawler
        await Crawler(
            worker_id=1,
            frontier=mock_frontier,
            client=mock_client,
            reporter=mock_reporter,
            max_pages_reached=max_pages_reached,
            max_pages=5,
        ).run()

    # Assertions
    mock_reporter.record.assert_not_called()  # Ensure record was not called
    mock_frontier.add_url.assert_not_called()  # Ensure no links were added
