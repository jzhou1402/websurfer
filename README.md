# NorCal Surf Adventures - West Coast Surfing Website

A beautiful surfing website showcasing Northern California's legendary surf spots with realistic URLs and hidden test scenarios for 404 errors and hanging requests.

## Features

- ✅ **Working Pages**: Beautiful surf website with real NorCal content
- ❌ **404 Error Links**: Realistic missing surf spots and services
- ⏳ **Hanging Links**: Surf guides that cause requests to hang or timeout
- 🌊 **Surf Theme**: Complete NorCal surfing experience

## Quick Start

1. **Start the server**:
   ```bash
   python3 server.py
   ```

2. **Open your browser** and go to:
   ```
   http://localhost:8000
   ```

3. **Explore the surf website** and test different scenarios by clicking various links.

## Available Pages

### Working Pages (200 OK)
- `/` - Home page (beautiful NorCal surf website)
- `/spots` - Surf spots overview page
- `/conditions` - Surf conditions and reports
- `/gear` - Surf gear guides
- `/about` - About page
- `/contact` - Contact information

### 404 Error Pages (404 Not Found)
These realistic surf spots and services will return 404 errors:
- `/spots/pleasure-point` - Pleasure Point surf spot
- `/spots/rockaway` - Rockaway Beach surf spot
- `/spots/ob` - Ocean Beach surf spot
- `/spots/linda-mar` - Linda Mar surf spot
- `/category/big-wave` - Big wave surfing category
- `/category/point-breaks` - Point breaks category
- `/category/beach-breaks` - Beach breaks category
- `/category/reef-breaks` - Reef breaks category
- `/category/beginner-friendly` - Beginner friendly spots
- `/category/advanced` - Advanced spots
- `/category/winter-spots` - Winter surf spots
- `/category/summer-spots` - Summer surf spots
- `/services/surf-lessons` - Surf lessons
- `/services/board-rental` - Board rental
- `/services/wetsuit-rental` - Wetsuit rental
- `/services/surf-guides` - Surf guides
- `/services/safety-courses` - Safety courses
- `/services/competitions` - Surf competitions
- `/newsletter` - Surf report newsletter
- `/instagram` - Instagram page
- `/youtube` - YouTube channel
- `/facebook` - Facebook page
- `/twitter` - Twitter page
- `/surfline` - Surfline integration
- `/privacy-policy` - Privacy policy
- `/terms-of-service` - Terms of service
- `/sitemap` - Sitemap
- `/advertising` - Advertising
- `/partnerships` - Partnerships

### Hanging Pages (Never Respond)
These surf guides will cause hanging requests:
- `/spots/mavericks` - Hangs forever (like a big wave that never comes)
- `/spots/steamer-lane` - 30-second delay
- `/spots/stinson-beach` - Infinite loop
- `/spots/fort-point` - 10-second delay
- `/gear/equipment-guide` - 60-second delay
- `/conditions/reports` - 45-second delay

## Featured NorCal Surf Spots

### 🏄‍♂️ Mavericks - Expert Level
Located off the coast of Half Moon Bay, Mavericks is one of the most challenging big wave surf spots in the world. With waves reaching up to 60 feet, this legendary break is only for the most experienced surfers.

### 🏄‍♀️ Steamer Lane - Advanced Level
Steamer Lane in Santa Cruz is a world-famous right-hand point break that offers consistent waves year-round. This spot is known for its long, peeling waves and is a favorite among experienced surfers.

### 🏖️ Stinson Beach - Intermediate Level
Stinson Beach offers a more forgiving surf experience perfect for intermediate surfers and families. Located in Marin County, this beach break provides consistent waves and a beautiful setting.

### 🏰 Fort Point - Advanced Level
Fort Point, located directly under the Golden Gate Bridge, offers a unique urban surfing experience. This powerful right-hand point break works best on large northwest swells and provides challenging waves in an iconic San Francisco setting.

## Testing Scenarios

### 404 Errors
Click any of the surf spot or service links in the sidebar to see custom 404 error pages with:
- Surf-themed styling
- "Surf Spot Not Found" message
- Requested path display
- Link back to home page

### Hanging Requests
Click the "Read More" links on the main surf spot posts to test:
- **Browser timeout handling**
- **Request cancellation**
- **Network error handling**

⚠️ **Warning**: Some hanging links will never respond and may require you to:
- Close the browser tab
- Cancel the request manually
- Restart the server

### Working Pages
- **Home Page**: Beautiful surf website with featured NorCal spots
- **Surf Spots Page**: Overview of available surf guides
- **Conditions**: Real-time surf reports and weather
- **Gear**: Equipment and technique guides
- **About**: Information about the surf website
- **Contact**: Contact information and social links

## Website Design

The website features:
- **Ocean Theme**: Beautiful blue gradient backgrounds inspired by the Pacific
- **Surf Styling**: Wave icons, surf terminology, and coastal colors
- **Difficulty Levels**: Color-coded difficulty badges for each surf spot
- **Responsive Layout**: Works on desktop and mobile devices
- **Professional Design**: Cards, hover effects, and smooth transitions
- **Navigation**: Sticky header with easy navigation
- **Sidebar**: Popular surf spots, categories, and services

## Server Information

- **Port**: 8000 (configurable in `server.py`)
- **Protocol**: HTTP
- **Framework**: Python built-in `http.server`
- **Features**: Custom request handling, surf-themed error pages, hanging request simulation

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## Customization

You can modify the server behavior by editing `server.py`:
- Change the port number
- Add new surf spots
- Modify response times for hanging requests
- Customize error pages
- Add more working pages

## Requirements

- Python 3.6+
- No external dependencies required

## Files

- `index.html` - Beautiful NorCal surf website homepage
- `server.py` - Python HTTP server with surf-themed request handling
- `README.md` - This documentation

## Hidden Test Features

This website appears to be a normal surf website but contains hidden test scenarios:
- **Realistic URLs**: All links look like they could exist on a real surf website
- **Hidden 404s**: Many sidebar links return 404 errors
- **Hidden Hanging**: Main surf spot links cause hanging requests
- **Seamless Integration**: Test scenarios are integrated naturally into the surf theme

## Deployment

See `DEPLOYMENT.md` for instructions on hosting this website online for free using various platforms like Render, PythonAnywhere, Railway, or Fly.io. 