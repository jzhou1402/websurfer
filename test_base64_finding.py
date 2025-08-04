#!/usr/bin/env python3
"""
Test script to demonstrate finding base64 links with requests + BeautifulSoup
"""

import requests
from bs4 import BeautifulSoup
import base64

def find_base64_links():
    """Find all base64 encoded links on the page"""
    
    # Get the page
    response = requests.get('http://localhost:8000')
    soup = BeautifulSoup(response.content, 'html.parser')
    
    print("🔍 Finding Base64 Links with Requests + BeautifulSoup")
    print("=" * 60)
    
    # 1. Find visible base64 hints
    print("\n📝 VISIBLE BASE64 HINTS:")
    base64_hints = soup.find_all('div', class_='base64-hint')
    for i, hint in enumerate(base64_hints, 1):
        encoded = hint.text.replace('Hidden: ', '')
        try:
            decoded = base64.b64decode(encoded).decode('utf-8')
            print(f"  {i}. Encoded: {encoded}")
            print(f"     Decoded: {decoded}")
        except:
            print(f"  {i}. Encoded: {encoded} (invalid base64)")
    
    # 2. Summary
    total_visible = len(base64_hints)
    
    print(f"\n📊 SUMMARY:")
    print(f"  Visible hints found: {total_visible}")
    print(f"  CSS-hidden links found: 0 (removed)")
    print(f"  Total base64 links: {total_visible}")
    print(f"  Dynamic links (requires Selenium): 2")

if __name__ == "__main__":
    find_base64_links() 