#!/usr/bin/env python3
"""
Simple BFS Web Scraper for localhost:8000
Quick and easy to use version
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import time

def scrape_links_bfs(start_url="http://localhost:8000/", max_pages=20):
    """
    Simple BFS scraper that finds all links from a starting URL
    
    Args:
        start_url (str): URL to start crawling from
        max_pages (int): Maximum number of pages to crawl
    
    Returns:
        list: All discovered links
    """
    visited = set()
    queue = deque([start_url])
    all_links = set()
    
    print(f"Starting BFS crawl from: {start_url}")
    print(f"Max pages: {max_pages}")
    print("-" * 40)
    
    while queue and len(visited) < max_pages:
        current_url = queue.popleft()
        
        if current_url in visited:
            continue
            
        print(f"Crawling: {current_url}")
        
        try:
            # Small delay to be respectful
            time.sleep(0.1)
            
            response = requests.get(current_url, timeout=5)
            response.raise_for_status()
            
            visited.add(current_url)
            
            # Parse HTML and extract links
            soup = BeautifulSoup(response.text, 'html.parser')
            page_links = set()
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                absolute_url = urljoin(current_url, href)
                page_links.add(absolute_url)
                all_links.add(absolute_url)
            
            print(f"  ✓ Found {len(page_links)} links")
            
            # Add new URLs to queue (only from same domain)
            base_domain = urlparse(start_url).netloc
            for link in page_links:
                try:
                    parsed = urlparse(link)
                    if (parsed.netloc == base_domain and 
                        link not in visited and 
                        link not in queue):
                        queue.append(link)
                except:
                    continue
                    
        except Exception as e:
            print(f"  ✗ Error: {e}")
            visited.add(current_url)
    
    print("-" * 40)
    print(f"Crawling completed!")
    print(f"Pages crawled: {len(visited)}")
    print(f"Total unique links: {len(all_links)}")
    
    return sorted(list(all_links))

if __name__ == "__main__":
    # Run the scraper
    links = scrape_links_bfs()
    
    print("\nAll discovered links:")
    for i, link in enumerate(links, 1):
        print(f"{i:2d}. {link}") 