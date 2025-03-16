# Monzo Web Crawler

## TODO
- [x] Add a `requirements.txt` file
- [ ] Add sequence diagram and architecture diagram

## Description

## Architecture

## Running

### Installation

To install the required dependencies, run the following command:
```bash
pip install -r requirements.txt
```

### Running the crawler

To run the crawler, run the following command:
```bash
python -m src.main # TODO: this doesnt work
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
