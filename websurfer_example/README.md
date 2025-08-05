# BFS Web Scraper

A Python web scraper that uses Breadth-First Search (BFS) to crawl localhost:8000 and discover all links, saving them to a `results.txt` file.

## Features

- **BFS Crawling**: Uses breadth-first search algorithm to systematically discover links
- **Domain Restriction**: Only crawls links within the same domain (localhost:8000)
- **Configurable Depth**: Set maximum crawl depth to control how far the scraper goes
- **Rate Limiting**: Built-in delays between requests to be respectful to the server
- **Error Handling**: Robust error handling for network issues and malformed URLs
- **Results Export**: Saves all discovered links to a formatted text file

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Make sure your localhost:8000 server is running
2. Run the scraper:
```bash
python web_scraper.py
```

The scraper will:
- Start crawling from `http://localhost:8000`
- Use BFS to discover all accessible links
- Save results to `results.txt`

## Configuration

You can modify the scraper behavior by editing the parameters in `web_scraper.py`:

- `max_depth`: Maximum depth to crawl (default: 3)
- `delay`: Delay between requests in seconds (default: 0.5)

## Output

The `results.txt` file will contain:
- A header with crawl information
- Total number of links found
- A numbered list of all discovered URLs

## Example Output

```
BFS Web Scraper Results for http://localhost:8000
Total links found: 15
============================================================

  1. http://localhost:8000/
  2. http://localhost:8000/about
  3. http://localhost:8000/contact
  4. http://localhost:8000/products
  5. http://localhost:8000/products/item1
  ...
```

## Notes

- The scraper respects robots.txt conventions
- It skips non-content files (images, CSS, JS, etc.)
- It only crawls HTTP/HTTPS URLs
- The scraper can be interrupted with Ctrl+C and will save partial results 