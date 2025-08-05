#!/usr/bin/env python3
"""
BFS Web Scraper for localhost:8000
Crawls the website using breadth-first search and saves all discovered links to results.txt
"""

import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from collections import deque
import time
import re
import signal
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
import base64

class BFSWebScraper:
    def __init__(self, base_url, max_depth=3, delay=1):
        """
        Initialize the BFS web scraper
        
        Args:
            base_url (str): The starting URL to crawl
            max_depth (int): Maximum depth to crawl
            delay (float): Delay between requests in seconds
        """
        self.base_url = base_url
        self.max_depth = max_depth
        self.delay = delay
        self.visited = set()
        self.queue = deque([(base_url, 0)])  # (url, depth)
        self.all_links = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        # Configure session for better timeout handling
        self.session.timeout = (2, 5)  # (connect_timeout, read_timeout) - much shorter
        # Disable SSL verification for localhost
        self.session.verify = False
        # Suppress SSL warnings
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # Thread pool for handling requests
        self.executor = ThreadPoolExecutor(max_workers=1)
    
    def is_valid_url(self, url):
        """Check if URL is valid (including external URLs)"""
        try:
            parsed = urlparse(url)
            
            # Skip non-HTTP/HTTPS URLs
            if parsed.scheme not in ['http', 'https']:
                return False
            
            # Skip common non-content URLs
            skip_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.css', '.js', '.xml', '.zip', '.tar', '.gz']
            if any(url.lower().endswith(ext) for ext in skip_extensions):
                return False
            
            return True
        except:
            return False
    
    def extract_links(self, url, html_content):
        """Extract all links from HTML content including dynamic ones"""
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []
        
        # Extract links from <a> tags
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(url, href)
            
            if self.is_valid_url(absolute_url):
                links.append(absolute_url)
        
        # Extract links from JavaScript (common patterns)
        js_patterns = [
            r'["\']([^"\']*\.php[^"\']*)["\']',  # PHP files
            r'["\']([^"\']*\.html?[^"\']*)["\']',  # HTML files
            r'["\']([^"\']*\.js[^"\']*)["\']',  # JS files
            r'["\']([^"\']*\.json[^"\']*)["\']',  # JSON endpoints
            r'["\']([^"\']*\.xml[^"\']*)["\']',  # XML endpoints
            r'["\']([^"\']*api/[^"\']*)["\']',  # API endpoints
            r'["\']([^"\']*ajax/[^"\']*)["\']',  # AJAX endpoints
            r'["\']([^"\']*\/[a-zA-Z0-9_-]+\/[^"\']*)["\']',  # General path patterns
            r'["\']([^"\']*\?[^"\']*)["\']',  # URLs with query parameters
        ]
        
        for pattern in js_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                if match.startswith('http'):
                    absolute_url = match
                else:
                    absolute_url = urljoin(url, match)
                
                if self.is_valid_url(absolute_url):
                    links.append(absolute_url)
        
        # Extract links from data attributes
        for element in soup.find_all(attrs={'data-url': True}):
            href = element['data-url']
            absolute_url = urljoin(url, href)
            if self.is_valid_url(absolute_url):
                links.append(absolute_url)
        
        for element in soup.find_all(attrs={'data-href': True}):
            href = element['data-href']
            absolute_url = urljoin(url, href)
            if self.is_valid_url(absolute_url):
                links.append(absolute_url)
        
        # Extract links from onclick attributes
        onclick_pattern = r'onclick=["\']([^"\']*)["\']'
        onclick_matches = re.findall(onclick_pattern, html_content, re.IGNORECASE)
        for match in onclick_matches:
            # Look for URLs in onclick handlers
            url_matches = re.findall(r'["\']([^"\']*\.(?:php|html?|js|json|xml)[^"\']*)["\']', match)
            for url_match in url_matches:
                absolute_url = urljoin(url, url_match)
                if self.is_valid_url(absolute_url):
                    links.append(absolute_url)
        
        # Extract links from form actions
        for form in soup.find_all('form', action=True):
            action = form['action']
            absolute_url = urljoin(url, action)
            if self.is_valid_url(absolute_url):
                links.append(absolute_url)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_links = []
        for link in links:
            if link not in seen:
                seen.add(link)
                unique_links.append(link)
        
        return unique_links
    
    def decode_base64_url(self, url):
        """Decode base64-encoded URLs if possible"""
        try:
            # Check if URL contains /decode/ followed by base64
            if '/decode/' in url:
                parts = url.split('/decode/')
                if len(parts) == 2:
                    encoded_part = parts[1]
                    # Try to decode the base64 part
                    decoded_bytes = base64.b64decode(encoded_part)
                    decoded_path = decoded_bytes.decode('utf-8')
                    return decoded_path
        except:
            pass
        return url
    
    def make_request_with_timeout(self, url, timeout=10):
        """Make a request with strict timeout handling"""
        try:
            future = self.executor.submit(self.session.get, url, timeout=(1, timeout))
            response = future.result(timeout=timeout + 2)  # Add buffer for thread overhead
            return response
        except FutureTimeoutError:
            print(f"Request timeout for {url} (thread timeout)")
            return None
        except Exception as e:
            print(f"Request error for {url}: {e}")
            return None
    
    def crawl(self):
        """Perform BFS crawling"""
        print(f"Starting BFS crawl of {self.base_url}")
        print(f"Max depth: {self.max_depth}")
        print("-" * 50)
        
        crawled_count = 0
        error_count = 0
        
        while self.queue:
            current_url, depth = self.queue.popleft()
            
            if current_url in self.visited or depth > self.max_depth:
                continue
            
            print(f"Crawling (depth {depth}): {current_url}")
            self.visited.add(current_url)
            
            try:
                # Use the timeout-protected request method
                response = self.make_request_with_timeout(current_url, timeout=1)
                
                if response is None:
                    print(f"Failed to get response for {current_url}")
                    self.visited.add(current_url)
                    error_count += 1
                    continue
                
                response.raise_for_status()
                
                # Add current URL to all_links
                self.all_links.add(current_url)
                
                # Extract and add new links
                if depth < self.max_depth:
                    links = self.extract_links(current_url, response.text)
                    for link in links:
                        # Add all valid links to results
                        self.all_links.add(link)
                        
                        # Only crawl internal links (same domain)
                        parsed = urlparse(link)
                        base_parsed = urlparse(self.base_url)
                        if parsed.netloc == base_parsed.netloc and link not in self.visited:
                            self.queue.append((link, depth + 1))
                            
                            # Also crawl decoded version if it's a base64 URL
                            if '/decode/' in link:
                                decoded_url = self.decode_base64_url(link)
                                if decoded_url != link:
                                    # Construct full decoded URL
                                    if decoded_url.startswith('/'):
                                        decoded_full_url = self.base_url + decoded_url
                                    else:
                                        decoded_full_url = urljoin(self.base_url, decoded_url)
                                    
                                    # Add decoded URL to results and crawl queue
                                    self.all_links.add(decoded_full_url)
                                    if decoded_full_url not in self.visited:
                                        self.queue.append((decoded_full_url, depth + 1))
                
                # Delay between requests
                time.sleep(self.delay)
                crawled_count += 1
                
            except requests.exceptions.Timeout:
                print(f"Timeout error crawling {current_url}")
                self.visited.add(current_url)  # Mark as visited to avoid infinite retries
                error_count += 1
            except requests.exceptions.ConnectionError:
                print(f"Connection error crawling {current_url}")
                self.visited.add(current_url)  # Mark as visited to avoid infinite retries
                error_count += 1
            except requests.exceptions.RequestException as e:
                print(f"Request error crawling {current_url}: {e}")
                self.visited.add(current_url)  # Mark as visited to avoid infinite retries
                error_count += 1
            except Exception as e:
                print(f"Unexpected error crawling {current_url}: {e}")
                self.visited.add(current_url)  # Mark as visited to avoid infinite retries
                error_count += 1
        
        print("-" * 50)
        print(f"Crawling completed!")
        print(f"Successfully crawled: {crawled_count} URLs")
        print(f"Errors encountered: {error_count} URLs")
        print(f"Total unique links found: {len(self.all_links)}")
    
    def save_results(self, filename="results.txt"):
        """Save all discovered links to a file"""
        with open(filename, 'w', encoding='utf-8') as f:
            for link in sorted(self.all_links):
                # Convert full URLs to relative paths for internal links
                if link.startswith(self.base_url):
                    relative_path = link[len(self.base_url):]
                    if not relative_path:
                        relative_path = "/"
                    
                    # Remove trailing slash (except for root path)
                    if relative_path != "/" and relative_path.endswith("/"):
                        relative_path = relative_path[:-1]
                    
                    # Decode base64 URLs if present
                    decoded_path = self.decode_base64_url(relative_path)
                    if decoded_path != relative_path:
                        # Remove trailing slash from decoded path too
                        if decoded_path != "/" and decoded_path.endswith("/"):
                            decoded_path = decoded_path[:-1]
                        f.write(f"{relative_path} -> {decoded_path}\n")
                    else:
                        f.write(f"{relative_path}\n")
                else:
                    # Remove trailing slash from external URLs too
                    if link.endswith("/"):
                        link = link[:-1]
                    f.write(f"{link}\n")
        
        print(f"Results saved to {filename}")
    
    def cleanup(self):
        """Clean up resources"""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print('\nReceived interrupt signal. Shutting down gracefully...')
    sys.exit(0)

def main():
    """Main function to run the scraper"""
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    base_url = "http://localhost:8000"
    
    # Test if the server is reachable first
    print("Testing connection to localhost:8000...")
    try:
        test_response = requests.get(base_url, timeout=5, verify=False)
        print(f"✓ Server is reachable (Status: {test_response.status_code})")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to localhost:8000. Make sure your server is running.")
        return
    except requests.exceptions.Timeout:
        print("✗ Connection to localhost:8000 timed out.")
        return
    except Exception as e:
        print(f"✗ Error testing connection: {e}")
        return
    
    # Create scraper instance
    scraper = BFSWebScraper(
        base_url=base_url,
        max_depth=3,  # Adjust this value to control crawl depth
        delay=0.5     # Adjust this value to control request rate
    )
    
    try:
        # Perform the crawl
        scraper.crawl()
        
        # Save results
        scraper.save_results("results.txt")
        
        print("\nScraping completed successfully!")
        print("Check results.txt for all discovered links.")
        
    except KeyboardInterrupt:
        print("\nCrawling interrupted by user.")
        print("Saving partial results...")
        scraper.save_results("results.txt")
    except Exception as e:
        print(f"An error occurred: {e}")
        # Try to save partial results even if there's an error
        try:
            scraper.save_results("results.txt")
            print("Partial results saved to results.txt")
        except:
            pass
    finally:
        # Always cleanup resources
        scraper.cleanup()

if __name__ == "__main__":
    main() 