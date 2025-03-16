# Monzo Web Crawler

## Description

This is a simple python web crawler which crawls a website and returns a list of all the pages listed on the website.

The web crawler uses concurrency with asyncio to speed up the crawling process. It uses a queue to manage the URLs to
crawl and a set to keep track of the URLs that have already been crawled. The program will stop crawling once it has
reached the maximum number of pages specified, or when there are no more pages to crawl.

This is possible through the use of a `max_pages_reached: asyncio.Event` object which is set when the maximum number of
pages has been reached. This event is checked by each worker before they start crawling a new page, and if it is set,
they will stop.

## Architecture

## TODO

- [x] Add a `requirements.txt` file
- [ ] Add sequence diagram and architecture diagram
- [ ] Relative URLs?

## Running

### Installation

To install the required dependencies, run the following command:
```bash
pip install -r requirements.txt
```

### Running the crawler

To run the crawler, run the following command:
```bash
python -m src.main # TODO: this doesnt work because of $PYTHONPATH
```

You can also add the following optional arguments:
- `--url`: The URL to start the crawl from. Default is `https://monzo.com`.
- `--workers`: The number of workers to use. Default is 5.
- `--max-pages`: The maximum number of pages to crawl. Default is 10.

### Pre-commit hook

To install the pre-commit hook, run the following command:
```bash
pip install pre-commit
pre-commit install
```

This will make sure that the code is linted and formatted before each commit.

## Testing

To run the tests, run the following command:
```bash
pytest
```

## Assumptions and Limitations

- It is technically possible that the program will return more than the maximum number of pages specified. This is
  because with multiple workers, it is possible that the max_pages_reached event is triggered while some workers are
  still processing their current page. This is a limitation of the current implementation.
- The program does not check robots.txt. This is a limitation of the current implementation and should be added in the
  future.
