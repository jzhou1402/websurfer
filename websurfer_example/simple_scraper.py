#!/usr/bin/env python3
"""
Simple BFS Web Scraper for localhost:8000
Alternative version with very aggressive timeouts to prevent hanging
"""

import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from collections import deque
import time
import signal
import sys
import base64

class SimpleBFSWebScraper:
    def __init__(self, base_url, max_depth=3, delay=0.5):
        self.base_url = base_url
        self.max_depth = max_depth
        self.delay = delay
        self.visited = set()
        self.queue = deque([(base_url, 0)])
        self.all_links = set()
        
        # Create session with very aggressive timeouts
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; SimpleScraper/1.0)'
        })
        # Very short timeouts to prevent hanging
        self.session.timeout = (1, 3)  # 1s connect, 3s read
        self.session.verify = False
        
        # Suppress SSL warnings
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def is_valid_url(self, url):
        try:
            parsed = urlparse(url)
            
            if parsed.scheme not in ['http', 'https']:
                return False
            
            skip_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.css', '.js', '.xml', '.zip']
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
    
    def safe_request(self, url):
        """Make a request with multiple fallback strategies"""
        strategies = [
            # Strategy 1: Very short timeout
            lambda: self.session.get(url, timeout=(0.5, 2)),
            # Strategy 2: Even shorter timeout
            lambda: self.session.get(url, timeout=(0.3, 1)),
            # Strategy 3: Head request only
            lambda: self.session.head(url, timeout=(0.5, 2))
        ]
        
        for i, strategy in enumerate(strategies):
            try:
                response = strategy()
                if hasattr(response, 'text') or response.status_code < 400:
                    return response
            except:
                continue
        
        return None
    
    def crawl(self):
        print(f"Starting simple BFS crawl of {self.base_url}")
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
            
            # Try to get the page
            response = self.safe_request(current_url)
            
            if response is None:
                print(f"Failed to get {current_url}")
                error_count += 1
                continue
            
            try:
                # Add current URL to all_links
                self.all_links.add(current_url)
                
                # Extract and add new links (only if we have text content)
                if depth < self.max_depth and hasattr(response, 'text'):
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
                
                crawled_count += 1
                
            except Exception as e:
                print(f"Error processing {current_url}: {e}")
                error_count += 1
            
            # Small delay
            time.sleep(self.delay)
        
        print("-" * 50)
        print(f"Crawling completed!")
        print(f"Successfully crawled: {crawled_count} URLs")
        print(f"Errors encountered: {error_count} URLs")
        print(f"Total unique links found: {len(self.all_links)}")
    
    def save_results(self, filename="results.txt"):
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

def signal_handler(sig, frame):
    print('\nReceived interrupt signal. Shutting down...')
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    base_url = "http://localhost:8000"
    
    # Quick connection test
    print("Testing connection to localhost:8000...")
    try:
        test_response = requests.get(base_url, timeout=2, verify=False)
        print(f"✓ Server is reachable (Status: {test_response.status_code})")
    except:
        print("✗ Cannot connect to localhost:8000. Make sure your server is running.")
        return
    
    scraper = SimpleBFSWebScraper(
        base_url=base_url,
        max_depth=3,
        delay=0.2  # Very short delay
    )
    
    try:
        scraper.crawl()
        scraper.save_results("results.txt")
        print("\nScraping completed successfully!")
        print("Check results.txt for all discovered links.")
        
    except KeyboardInterrupt:
        print("\nCrawling interrupted by user.")
        scraper.save_results("results.txt")
    except Exception as e:
        print(f"An error occurred: {e}")
        try:
            scraper.save_results("results.txt")
            print("Partial results saved to results.txt")
        except:
            pass

if __name__ == "__main__":
    main() 