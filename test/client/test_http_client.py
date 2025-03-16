from unittest.mock import patch, AsyncMock

import aiohttp
import pytest
from aioresponses import aioresponses

from src.client.http_client import Client


@pytest.fixture
def client():
    """Fixture to create a Client instance."""
    return Client(allowed_netloc="example.com")


async def test_fetch_success(client):
    """Test successful fetch of a URL."""
    url = "https://example.com/page1"
    content = "<html><body>Hello, World!</body></html>"

    with aioresponses() as m:
        # Mock a successful response
        m.get(url, status=200, body=content, headers={"Content-Type": "text/html"})

        # Call the fetch method
        final_url, fetched_content = await client.fetch(url)

        # Assertions
        assert final_url == url
        assert fetched_content == content


async def test_fetch_non_html_content(client):
    """Test fetching non-HTML content."""
    url = "https://example.com/image.png"
    content = "binary data"

    with aioresponses() as m:
        # Mock a response with non-HTML content
        m.get(url, status=200, body=content, headers={"Content-Type": "image/png"})

        # Call the fetch method
        final_url, fetched_content = await client.fetch(url)

        # Assertions
        assert final_url is None
        assert fetched_content is None


async def test_fetch_http_error(client):
    """Test fetching a URL that returns an HTTP error."""
    url = "https://example.com/error"

    with aioresponses() as m:
        # Mock a 404 error response
        m.get(url, status=404)

        # Call the fetch method
        final_url, fetched_content = await client.fetch(url)

        # Assertions
        assert final_url is None
        assert fetched_content is None


async def test_fetch_network_error(client):
    """Test fetching a URL that causes a network error."""
    url = "https://example.com/network-error"

    with aioresponses() as m:
        # Mock a network error (e.g., connection timeout)
        m.get(url, exception=aiohttp.ClientError("Network error"))

        # Call the fetch method
        final_url, fetched_content = await client.fetch(url)

        # Assertions
        assert final_url is None
        assert fetched_content is None


async def test_close_session(client):
    """Test closing the aiohttp session."""
    # Create a mock session
    with patch("aiohttp.ClientSession") as mock_session:
        mock_session.return_value = mock_session
        mock_session.close = AsyncMock()

        # Simulate session creation by calling fetch
        with aioresponses() as m:
            m.get(
                "https://example.com/page1",
                status=200,
                body="<html></html>",
                headers={"Content-Type": "text/html"},
            )
            await client.fetch("https://example.com/page1")

        # Call the close method
        await client.close()

        # Assertions
        mock_session.close.assert_called_once()
