# Monzo Web Crawler

## Description

This is a simple python web crawler which crawls a website and returns a list of all the pages listed on the website.

The web crawler uses concurrency with asyncio to speed up the crawling process. It uses a queue to manage the URLs to
crawl and a set to keep track of the URLs that have already been crawled. The program will stop crawling once it has
reached the maximum number of pages specified, or when there are no more pages to crawl.

This is possible through the use of a `max_pages_reached: asyncio.Event` object which is set when the maximum number of
pages has been reached. This event is checked by each worker before they start crawling a new page, and if it is set,
they will stop.

As the program uses asyncio, all the workers run on a single thread.

## Architecture

The web crawler consists of the following components:

- **Frontier**: Manages the queue of URLs to crawl and ensures URLs are not visited multiple times.
- **Client**: Handles HTTP requests to fetch web pages.
- **Parser**: Extracts links from HTML content.
- **Reporter**: Records the results of the crawl (e.g., URLs and their links).
- **Crawler**: Orchestrates the crawling process by coordinating the other components.

### Asyncio and the Global Interpreter Lock (GIL)

Until Python 3.12, the Global Interpreter Lock (GIL) acted as a mutex that protected access to Python objects, meaning
that even if you had multiple threads, only one could execute Python code at a time. This is a limitation of the
language itself. One advantage of this approach is that it makes it easier to write thread-safe code, as the GIL ensures
acts as a mutex and any python bytecode requires acquiring the interpreter lock to execute. One big drawback is that
Python threads cannot take advantage of multiple cores.

With more recent versions of Python, the GIL has been relaxed, allowing for parallelism. This is achieved through
sub-interpreters, which are separate interpreters that run in separate threads with their own GIL.

With modern Python, there are many ways to achieve concurrency, each with their own trade-offs. However, this program
uses asyncio, or coroutines, which run on a single thread. This approach achieves concurrency, _but not parallelism_. As
the main bottleneck in this application is the network I/O, asyncio is a good choice for this. It is also extremely well
documented and easy to use.

## Running

### Requirements

- Python > 3.12
- Pip > 23.2.1
- [A virtualenv to install the dependencies](https://virtualenv.pypa.io/en/latest/user_guide.html)

### Installation

To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

### Running the crawler

To run the crawler, run the following command:

```bash
python -m src.main
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

- The program does not check robots.txt. This is a limitation of the current implementation and should be added in the
  future.
- Because each Crawler is its own task, and executes concurrently, this can lead to over-fetching. Meaning that even
  though the `max_pages_reached: asyncio.Event` event has already been set, a crawler might have already started to
  fetch the next page. This leads to scenarios where `max_pages = 10`, yet the `Client` will have fetched 14 pages. This
  won't be reflected in the `Reporter` as there is a maximum size implemented.

## Further reading

- https://docs.python.org/3/library/asyncio.html
- https://tonybaloney.github.io/posts/sub-interpreter-web-workers.html
- https://dev.to/welldone2094/async-programming-in-python-with-asyncio-12dl
