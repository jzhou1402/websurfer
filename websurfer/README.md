# BFS Web Scraper

A simple Breadth-First Search (BFS) web scraper to crawl all links from a website, specifically designed for scraping `http://localhost:8000/`.

## Features

- **BFS Algorithm**: Uses breadth-first search to systematically crawl all pages
- **Domain Restriction**: Only crawls links within the same domain
- **Rate Limiting**: Includes delays between requests to be respectful to servers
- **Error Handling**: Gracefully handles network errors and invalid URLs
- **Detailed Logging**: Shows progress and results in real-time
- **JSON Export**: Saves detailed results to a JSON file

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start (Simple Version)

Run the simple scraper for a quick test:

```bash
python simple_scraper.py
```

This will:
- Start crawling from `http://localhost:8000/`
- Crawl up to 20 pages by default
- Print all discovered links

### Full Version (Advanced)

Run the full-featured scraper:

```bash
python web_scraper.py
```

This will:
- Start crawling from `http://localhost:8000/`
- Crawl up to 50 pages by default
- Save detailed results to `crawl_results.json`
- Show comprehensive statistics

### Custom Configuration

You can modify the configuration in `web_scraper.py`:

```python
# Configuration
START_URL = "http://localhost:8000/"
MAX_PAGES = 50  # Adjust based on your needs
DELAY = 0.1     # Delay between requests in seconds
```

## Output

### Console Output
The scraper will show real-time progress:
```
Starting BFS crawl from: http://localhost:8000/
Base domain: localhost:8000
Max pages to crawl: 50
--------------------------------------------------
Crawling: http://localhost:8000/
  ✓ Status: 200
  ✓ Links found: 5
  ✓ Queue size: 4
```

### JSON Results
Detailed results are saved to `crawl_results.json`:
```json
{
  "start_url": "http://localhost:8000/",
  "visited_pages": [
    {
      "url": "http://localhost:8000/",
      "status_code": 200,
      "links_found": 5,
      "links": ["http://localhost:8000/page1", "http://localhost:8000/page2"]
    }
  ],
  "all_links": ["http://localhost:8000/page1", "http://localhost:8000/page2"],
  "total_pages_crawled": 1,
  "total_links_found": 2
}
```

## How BFS Works

1. **Start**: Begin with the starting URL in a queue
2. **Process**: Take the first URL from the queue
3. **Fetch**: Download the page content
4. **Extract**: Find all links on the page
5. **Filter**: Keep only valid URLs from the same domain
6. **Queue**: Add new URLs to the end of the queue
7. **Repeat**: Continue until queue is empty or limit reached

This ensures that:
- All pages at the same "depth" are visited before going deeper
- No page is visited twice
- The crawl is systematic and complete

## Safety Features

- **Rate Limiting**: Built-in delays prevent overwhelming the server
- **Domain Restriction**: Only crawls the specified domain
- **File Type Filtering**: Skips non-HTML files (images, PDFs, etc.)
- **Error Handling**: Continues crawling even if individual pages fail
- **Timeout Protection**: Prevents hanging on slow responses

## Troubleshooting

### Connection Refused
Make sure your localhost server is running on port 8000:
```bash
# Example: Start a simple Python server
python -m http.server 8000
```

### No Links Found
- Check if the server is serving HTML content
- Verify that links use `<a href="">` tags
- Ensure the server is accessible from your machine

### Too Many Requests
Increase the delay between requests:
```python
DELAY = 0.5  # 0.5 seconds between requests
```

## License

This project is open source and available under the MIT License. 