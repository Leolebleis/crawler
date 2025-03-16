import pytest

from service.parser import parse


@pytest.mark.parametrize(
    "base_url, link, expected",
    [
        ("https://monzo.com", "https://monzo.com/blog/", {"https://monzo.com/blog"}),
        ("https://monzo.com", "/blog/", {"https://monzo.com/blog"}),
        ("https://monzo.com", "https://example.com/", {"https://example.com"}),
        ("https://monzo.com", "mailto:monzo@gmail.com", set()),
    ],
)
def test_parse(base_url: str, link: str, expected: str) -> None:
    html = f"""
    <a href="{link}">Blog</a>
    """

    links = parse(base_url, html)
    assert links == expected
