import pytest

from src.utils import normalize_url


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://monzo.com", "https://monzo.com"),
        ("https://monzo.com/", "https://monzo.com"),
        ("https://monzo.com/about", "https://monzo.com/about"),
        ("https://monzo.com/about?", "https://monzo.com/about"),
    ],
)
def test_normalize_url(url: str, expected: str):
    result = normalize_url(url)
    assert result == expected
