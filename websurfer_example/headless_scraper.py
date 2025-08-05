#!/usr/bin/env python3
"""
Headless BFS Web Scraper for localhost:8000
Uses Selenium with Chrome headless to execute JavaScript and capture dynamic links
"""

import time
import signal
import sys
import base64
import re
from urllib.parse import urljoin, urlparse
from collections import deque
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

class HeadlessBFSWebScraper:
    def __init__(self, base_url, max_depth=3, delay=1, js_wait_time=3):
        """
        Initialize the headless BFS web scraper
        
        Args:
            base_url (str): The starting URL to crawl
            max_depth (int): Maximum depth to crawl
            delay (float): Delay between requests in seconds
            js_wait_time (float): Time to wait for JavaScript to load
        """
        self.base_url = base_url
        self.max_depth = max_depth
        self.delay = delay
        self.js_wait_time = js_wait_time
        self.visited = set()
        self.queue = deque([(base_url, 0)])
        self.all_links = set()
        
        # Setup Chrome options for headless browsing
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Initialize the driver
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Initialize the Chrome WebDriver"""
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.driver.set_page_load_timeout(10)
            print("✓ Chrome WebDriver initialized successfully")
        except Exception as e:
            print(f"✗ Failed to initialize Chrome WebDriver: {e}")
            print("Make sure Chrome and chromedriver are installed")
            sys.exit(1)
    
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
    
    def extract_links_from_dom(self, url):
        """Extract all links from the rendered DOM"""
        links = []
        
        try:
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Wait for JavaScript to execute
            time.sleep(self.js_wait_time)
            
            # Extract links from <a> tags
            anchor_elements = self.driver.find_elements(By.TAG_NAME, "a")
            for element in anchor_elements:
                try:
                    href = element.get_attribute("href")
                    if href and self.is_valid_url(href):
                        links.append(href)
                except:
                    continue
            
            # Extract links from JavaScript variables (from page source)
            page_source = self.driver.page_source
            
            # Look for common URL patterns in JavaScript
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
                matches = re.findall(pattern, page_source, re.IGNORECASE)
                for match in matches:
                    if match.startswith('http'):
                        absolute_url = match
                    else:
                        absolute_url = urljoin(url, match)
                    
                    if self.is_valid_url(absolute_url):
                        links.append(absolute_url)
            
            # Extract links from data attributes
            data_url_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-url]")
            for element in data_url_elements:
                try:
                    href = element.get_attribute("data-url")
                    if href:
                        absolute_url = urljoin(url, href)
                        if self.is_valid_url(absolute_url):
                            links.append(absolute_url)
                except:
                    continue
            
            data_href_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-href]")
            for element in data_href_elements:
                try:
                    href = element.get_attribute("data-href")
                    if href:
                        absolute_url = urljoin(url, href)
                        if self.is_valid_url(absolute_url):
                            links.append(absolute_url)
                except:
                    continue
            
            # Extract form actions
            form_elements = self.driver.find_elements(By.TAG_NAME, "form")
            for element in form_elements:
                try:
                    action = element.get_attribute("action")
                    if action:
                        absolute_url = urljoin(url, action)
                        if self.is_valid_url(absolute_url):
                            links.append(absolute_url)
                except:
                    continue
            
            # Remove duplicates while preserving order
            seen = set()
            unique_links = []
            for link in links:
                if link not in seen:
                    seen.add(link)
                    unique_links.append(link)
            
            return unique_links
            
        except TimeoutException:
            print(f"Timeout waiting for page to load: {url}")
            return []
        except Exception as e:
            print(f"Error extracting links from {url}: {e}")
            return []
    
    def crawl(self):
        """Perform BFS crawling with headless browser"""
        print(f"Starting headless BFS crawl of {self.base_url}")
        print(f"Max depth: {self.max_depth}")
        print(f"JavaScript wait time: {self.js_wait_time}s")
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
                # Navigate to the page
                self.driver.get(current_url)
                
                # Add current URL to all_links
                self.all_links.add(current_url)
                
                # Extract links from the rendered page
                if depth < self.max_depth:
                    links = self.extract_links_from_dom(current_url)
                    
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
                
            except TimeoutException:
                print(f"Timeout error crawling {current_url}")
                error_count += 1
            except WebDriverException as e:
                print(f"WebDriver error crawling {current_url}: {e}")
                error_count += 1
            except Exception as e:
                print(f"Unexpected error crawling {current_url}: {e}")
                error_count += 1
            
            # Delay between requests
            time.sleep(self.delay)
        
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
        if self.driver:
            self.driver.quit()

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print('\nReceived interrupt signal. Shutting down gracefully...')
    sys.exit(0)

def main():
    """Main function to run the scraper"""
    signal.signal(signal.SIGINT, signal_handler)
    
    base_url = "http://localhost:8000"
    
    # Test if the server is reachable first
    print("Testing connection to localhost:8000...")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        test_options = Options()
        test_options.add_argument("--headless")
        test_options.add_argument("--no-sandbox")
        test_options.add_argument("--disable-dev-shm-usage")
        
        test_driver = webdriver.Chrome(options=test_options)
        test_driver.set_page_load_timeout(5)
        test_driver.get(base_url)
        print(f"✓ Server is reachable (Title: {test_driver.title})")
        test_driver.quit()
    except Exception as e:
        print(f"✗ Cannot connect to localhost:8000: {e}")
        print("Make sure your server is running and Chrome/chromedriver are installed")
        return
    
    # Create scraper instance
    scraper = HeadlessBFSWebScraper(
        base_url=base_url,
        max_depth=3,      # Adjust this value to control crawl depth
        delay=0.5,        # Adjust this value to control request rate
        js_wait_time=3    # Adjust this value to control JS wait time
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