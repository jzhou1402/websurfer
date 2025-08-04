# Wanderlust Adventures - Travel Blog

A beautiful travel blog website with realistic URLs and hidden test scenarios for 404 errors and hanging requests.

## Features

- ✅ **Working Pages**: Beautiful travel blog with real content
- ❌ **404 Error Links**: Realistic missing travel destinations and services
- ⏳ **Hanging Links**: Travel guides that cause requests to hang or timeout
- 🌍 **Travel Theme**: Complete travel blog experience

## Quick Start

1. **Start the server**:
   ```bash
   python3 server.py
   ```

2. **Open your browser** and go to:
   ```
   http://localhost:8000
   ```

3. **Explore the travel blog** and test different scenarios by clicking various links.

## Available Pages

### Working Pages (200 OK)
- `/` - Home page (beautiful travel blog)
- `/destinations` - Destinations overview page
- `/travel-tips` - Travel tips and resources
- `/photography` - Photography guides
- `/about` - About page
- `/contact` - Contact information

### 404 Error Pages (404 Not Found)
These realistic travel destinations and services will return 404 errors:
- `/destinations/japan` - Japan travel guide
- `/destinations/iceland` - Iceland travel guide
- `/destinations/new-zealand` - New Zealand travel guide
- `/destinations/morocco` - Morocco travel guide
- `/destinations/peru` - Peru travel guide
- `/destinations/australia` - Australia travel guide
- `/destinations/croatia` - Croatia travel guide
- `/destinations/portugal` - Portugal travel guide
- `/category/adventure` - Adventure travel category
- `/category/culture` - Cultural experiences
- `/category/food` - Food & dining
- `/category/budget` - Budget travel
- `/category/luxury` - Luxury travel
- `/category/solo` - Solo travel
- `/category/family` - Family travel
- `/category/road-trip` - Road trips
- `/services/travel-insurance` - Travel insurance
- `/services/visa-assistance` - Visa assistance
- `/services/booking-support` - Booking support
- `/services/travel-consultation` - Travel consultation
- `/services/photography-workshops` - Photography workshops
- `/services/guided-tours` - Guided tours
- `/newsletter` - Newsletter signup
- `/instagram` - Instagram page
- `/youtube` - YouTube channel
- `/facebook` - Facebook page
- `/twitter` - Twitter page
- `/pinterest` - Pinterest page
- `/privacy-policy` - Privacy policy
- `/terms-of-service` - Terms of service
- `/sitemap` - Sitemap
- `/advertising` - Advertising
- `/partnerships` - Partnerships

### Hanging Pages (Never Respond)
These travel guides will cause hanging requests:
- `/destinations/swiss-alps-hiking-guide` - Hangs forever
- `/destinations/bali-hidden-beaches` - 30-second delay
- `/destinations/ancient-rome-guide` - Infinite loop
- `/destinations/bangkok-street-food` - 10-second delay
- `/travel-tips/planning-tools` - 60-second delay
- `/photography/equipment-guide` - 45-second delay

## Testing Scenarios

### 404 Errors
Click any of the destination or service links in the sidebar to see custom 404 error pages with:
- Travel-themed styling
- "Destination Not Found" message
- Requested path display
- Link back to home page

### Hanging Requests
Click the "Read More" links on the main blog posts to test:
- **Browser timeout handling**
- **Request cancellation**
- **Network error handling**

⚠️ **Warning**: Some hanging links will never respond and may require you to:
- Close the browser tab
- Cancel the request manually
- Restart the server

### Working Pages
- **Home Page**: Beautiful travel blog with featured destinations
- **Destinations Page**: Overview of available travel guides
- **Travel Tips**: Resources and planning tools
- **Photography**: Equipment and technique guides
- **About**: Information about the travel blog
- **Contact**: Contact information and social links

## Website Design

The website features:
- **Modern Design**: Beautiful gradient backgrounds and clean typography
- **Responsive Layout**: Works on desktop and mobile devices
- **Travel Theme**: Complete travel blog experience with realistic content
- **Professional Styling**: Cards, hover effects, and smooth transitions
- **Navigation**: Sticky header with easy navigation
- **Sidebar**: Popular destinations, categories, and services

## Server Information

- **Port**: 8000 (configurable in `server.py`)
- **Protocol**: HTTP
- **Framework**: Python built-in `http.server`
- **Features**: Custom request handling, travel-themed error pages, hanging request simulation

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## Customization

You can modify the server behavior by editing `server.py`:
- Change the port number
- Add new travel destinations
- Modify response times for hanging requests
- Customize error pages
- Add more working pages

## Requirements

- Python 3.6+
- No external dependencies required

## Files

- `index.html` - Beautiful travel blog homepage
- `server.py` - Python HTTP server with travel-themed request handling
- `README.md` - This documentation

## Hidden Test Features

This website appears to be a normal travel blog but contains hidden test scenarios:
- **Realistic URLs**: All links look like they could exist on a real travel website
- **Hidden 404s**: Many sidebar links return 404 errors
- **Hidden Hanging**: Main blog post links cause hanging requests
- **Seamless Integration**: Test scenarios are integrated naturally into the travel theme 