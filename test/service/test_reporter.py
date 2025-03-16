from _pytest.logging import LogCaptureFixture

from service.reporter import Reporter


def test_record_new_url() -> None:
    reporter = Reporter()

    url = "http://example.com"
    links = {"http://example.com/page1", "http://example.com/page2"}

    reporter.record(url, links)

    assert url in reporter.results
    assert reporter.results[url] == links

def test_output(caplog: LogCaptureFixture) -> None:
    reporter = Reporter()

    url = "http://example.com"
    links = {"http://example.com/page1", "http://example.com/page2"}
    reporter.record(url, links)

    with caplog.at_level("INFO"):
        reporter.output()

    assert "URL: http://example.com" in caplog.text
    assert "Links:" in caplog.text
    assert "  - http://example.com/page1" in caplog.text
    assert "  - http://example.com/page2" in caplog.text
