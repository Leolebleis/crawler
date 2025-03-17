from _pytest.logging import LogCaptureFixture

from service.reporter import Reporter


def test_record_new_url() -> None:
    reporter = Reporter(max_size=10)

    url = "http://example.com"
    links = {"http://example.com/page1", "http://example.com/page2"}

    reporter.record(url, links)

    assert url in reporter.results
    assert reporter.results[url] == links

def test_record_new_url_max_size_reached() -> None:
    max_size = 1
    reporter = Reporter(max_size=max_size)

    url = "http://example.com"
    links = {"http://example.com/page1", "http://example.com/page2"}
    reporter.record(url, links)

    url2 = "http://example.com/page1"
    reporter.record(url2, links)

    assert len(reporter.results) == max_size
    assert url in reporter.results
    assert reporter.results[url] == links
    assert url2 not in reporter.results

def test_output(caplog: LogCaptureFixture) -> None:
    reporter = Reporter(max_size=10)

    url = "http://example.com"
    links = {"http://example.com/page1", "http://example.com/page2"}
    reporter.record(url, links)

    with caplog.at_level("INFO"):
        reporter.output()

    assert "URL: http://example.com" in caplog.text
    assert "Links:" in caplog.text
    assert "  - http://example.com/page1" in caplog.text
    assert "  - http://example.com/page2" in caplog.text
