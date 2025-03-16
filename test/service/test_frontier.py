import pytest

from service.frontier import Frontier


@pytest.mark.parametrize(
    "url, expected, allowed_netloc",
    [
        ("https://monzo.com", "https://monzo.com", "monzo.com"),
        ("https://monzo.com/about", "https://monzo.com/about", "monzo.com"),
        ("https://monzo.com/about", None, "example.com"),
        ("https://monzo.com/about", None, ""),
        ("https://monzo.com/about", None, None),
    ],
)
async def test_frontier(url: str, expected: str, allowed_netloc: str) -> None:
    frontier = Frontier(allowed_netloc=allowed_netloc)

    await frontier.add_url(url)

    assert frontier.has_next() == bool(expected)

    assert await frontier.get_next_url() == expected
    expected_visited = [expected] if expected else []
    assert frontier._visited == set(expected_visited)

    assert not frontier.has_next()
