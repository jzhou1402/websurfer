#!/usr/bin/env python3
"""
Simple HTTP Server for NorCal Surf Adventures
Handles content, 404 errors, hanging requests, and base64 decoded pages
"""

import http.server
import socketserver
import os
import time
import base64

class SurfAdventuresHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests with custom routing"""
        path = self.path
        
        # Handle base64 decode redirects
        if path.startswith('/decode/'):
            self.handle_base64_redirect(path)
            return
        
        # Handle gallery pages
        if path == '/gallery/mavericks-photos/':
            self.send_gallery_page()
            return
        
        # Handle base64 decoded internal pages (leaf nodes)
        if path in ['/gear/wetsuit-guide/',
                   '/conditions/weather-reports/', '/spots/surf-reports/',
                   '/spots/tide-reports/', '/dynamic/surf-report/',
                   '/dynamic/forecast/']:
            self.send_base64_page(path)
            return
        
        # Handle hanging request
        if path == '/hang':
            self.send_hanging_response()
            return
        
        # Handle 404 errors for specific paths
        if path in ['/spots/mavericks/forecast', '/spots/mavericks', 
                   '/spots/steamer-lane', '/gear/equipment-guide',
                   '/conditions/reports', '/shop/boards/channel-islands',
                   '/dynamic/surf-report', '/dynamic/forecast']:
            self.send_404_response(path)
            return
        
        # Serve the main page for root and other paths
        if path == '/' or path == '/index.html':
            self.send_main_page()
            return
        
        # Serve the spots page
        if path == '/spots':
            self.send_spots_page()
            return
        
        # Serve the about page
        if path == '/about':
            self.send_about_page()
            return
        
        # Default to 404 for unknown paths
        self.send_404_response(path)

    def send_main_page(self):
        """Send the main HTML page"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Read and serve the index.html file
        try:
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.wfile.write(b"<h1>Error: index.html not found</h1>")

    def send_spots_page(self):
        """Send the spots HTML page"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Read and serve the spots.html file
        try:
            with open('spots.html', 'rb') as f:
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.wfile.write(b"<h1>Error: spots.html not found</h1>")

    def send_about_page(self):
        """Send the about HTML page"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Read and serve the about.html file
        try:
            with open('about.html', 'rb') as f:
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.wfile.write(b"<h1>Error: about.html not found</h1>")

    def handle_base64_redirect(self, path):
        """Handle base64 encoded redirects"""
        try:
            # Extract base64 string from path
            base64_string = path.replace('/decode/', '')
            
            # Decode the base64 string
            decoded_path = base64.b64decode(base64_string).decode('utf-8')
            
            # Redirect to the decoded path
            self.send_response(302)
            self.send_header('Location', decoded_path)
            self.end_headers()
            
        except Exception as e:
            # If decoding fails, send 404
            self.send_404_response(path)

    def send_gallery_page(self):
        """Send the gallery HTML page"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Read and serve the gallery HTML file
        try:
            with open('gallery/mavericks-photos.html', 'rb') as f:
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.wfile.write(b"<h1>Error: gallery/mavericks-photos.html not found</h1>")

    def send_404_response(self, path):
        """Send a 404 error response"""
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>404 - Page Not Found</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
                .error {{ color: #e74c3c; font-size: 3rem; margin-bottom: 1rem; }}
                .message {{ color: #666; font-size: 1.2rem; }}
            </style>
        </head>
        <body>
            <div class="error">🏄‍♂️ 404</div>
            <div class="message">Surf's up, but this page isn't here!</div>
            <div class="message">Path: {path}</div>
            <p><a href="/">← Back to Home</a></p>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode())

    def send_hanging_response(self):
        """Send a hanging response that never completes"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Send partial content and then hang
        self.wfile.write(b"<html><body><h1>Loading...</h1>")
        self.wfile.flush()
        
        # Keep the connection open indefinitely
        while True:
            time.sleep(1)
            try:
                self.wfile.write(b"<!-- still loading -->")
                self.wfile.flush()
            except:
                break

    def send_base64_page(self, path):
        """Send pages that are accessed via base64 decoded links (leaf nodes)"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Generate content based on the path
        if path == '/gallery/mavericks-photos/':
            title = "Mavericks Photo Gallery"
            content = """
            <h2>🏄‍♂️ Mavericks Photo Gallery</h2>
            <p>Amazing photos of the legendary big wave spot.</p>
            <div style="background: #f0f0f0; padding: 20px; border-radius: 10px;">
                <p>📸 Photo 1: 60-foot wave at Mavericks</p>
                <p>📸 Photo 2: Surfer riding the monster</p>
                <p>📸 Photo 3: Aerial view of the break</p>
            </div>
            """
        elif path == '/gear/wetsuit-guide/':
            title = "Wetsuit Guide"
            content = """
            <h2>🧥 NorCal Wetsuit Guide</h2>
            <p>Essential guide for staying warm in cold NorCal waters.</p>
            <div style="background: #f0f0f0; padding: 20px; border-radius: 10px;">
                <p>❄️ 4/3mm wetsuit for winter</p>
                <p>🌊 3/2mm wetsuit for summer</p>
                <p>🧤 Booties and gloves essential</p>
            </div>
            """
        elif path == '/conditions/weather-reports/':
            title = "Weather Reports"
            content = """
            <h2>🌤️ Weather Reports</h2>
            <p>Current weather conditions for all NorCal surf spots.</p>
            <div style="background: #f0f0f0; padding: 20px; border-radius: 10px;">
                <p>🌊 Mavericks: 15-20ft, offshore winds</p>
                <p>🏄‍♀️ Steamer Lane: 6-8ft, light winds</p>
                <p>🌡️ Water temp: 52°F</p>
            </div>
            """
        elif path == '/spots/surf-reports/':
            title = "Surf Reports"
            content = """
            <h2>🌊 Surf Reports</h2>
            <p>Real-time surf conditions and forecasts.</p>
            <div style="background: #f0f0f0; padding: 20px; border-radius: 10px;">
                <p>📊 Current swell: 8-12ft</p>
                <p>🌪️ Wind: NW 15mph</p>
                <p>⏰ Tide: High at 2:30 PM</p>
            </div>
            """
        elif path == '/spots/tide-reports/':
            title = "Tide Reports"
            content = """
            <h2>🌊 Tide Reports</h2>
            <p>Daily tide schedules for optimal surfing.</p>
            <div style="background: #f0f0f0; padding: 20px; border-radius: 10px;">
                <p>🌅 Low tide: 6:45 AM</p>
                <p>🌊 High tide: 2:30 PM</p>
                <p>🌅 Low tide: 7:15 PM</p>
            </div>
            """
        elif path == '/dynamic/surf-report/':
            title = "Dynamic Surf Report"
            content = """
            <h2>🌊 Dynamic Surf Report</h2>
            <p>Real-time conditions generated dynamically.</p>
            <div style="background: #f0f0f0; padding: 20px; border-radius: 10px;">
                <p>🔄 Updated: Just now</p>
                <p>🌊 Swell: 10-15ft</p>
                <p>💨 Wind: Variable</p>
            </div>
            """
        elif path == '/dynamic/forecast/':
            title = "Extended Forecast"
            content = """
            <h2>📅 Extended Forecast</h2>
            <p>7-day surf forecast for NorCal spots.</p>
            <div style="background: #f0f0f0; padding: 20px; border-radius: 10px;">
                <p>📆 Tomorrow: 12-18ft</p>
                <p>📆 Weekend: 8-12ft</p>
                <p>📆 Next week: 6-10ft</p>
            </div>
            """
        else:
            title = "Unknown Page"
            content = "<p>This page was accessed via base64 decoding.</p>"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title} - NorCal Surf Adventures</title>
            <style>
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #74b9ff 100%);
                    margin: 0;
                    padding: 2rem;
                    min-height: 100vh;
                    color: white;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: rgba(255, 255, 255, 0.1);
                    padding: 2rem;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                }}
                h1 {{ color: white; margin-bottom: 1rem; }}
                h2 {{ color: #74b9ff; margin-bottom: 1rem; }}
                p {{ line-height: 1.6; margin-bottom: 1rem; }}
                a {{ color: #74b9ff; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{title}</h1>
                <div class="content">
                    {content}
                </div>
                <p style="text-align: center; margin-top: 2rem;">
                    <a href="/" style="padding: 0.5rem 1rem; border: 2px solid #74b9ff; border-radius: 5px;">← Back to Home</a>
                </p>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode())

def run_server(port=None):
    """Run the HTTP server"""
    if port is None:
        port = int(os.environ.get('PORT', 8000))
    
    handler = SurfAdventuresHTTPRequestHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print("🏄‍♂️ NorCal Surf Adventures Server")
        print("=" * 50)
        print(f"Server running on port {port}")
        print(f"Website: http://localhost:{port}")
        print()
        print("📋 Available Routes:")
        print("   - Main page: /")
        print("   - Surf spots page: /spots")
        print("   - About page: /about")
        print("   - Gallery page: /gallery/mavericks-photos/")
        print("   - 404 errors: /spots/mavericks/forecast, /spots/mavericks, etc.")
        print("   - Hanging request: /hang")
        print("   - Base64 decoded pages: /gear/wetsuit-guide/, etc.")
        print("   - Dynamic pages: /dynamic/surf-report/, /dynamic/forecast/")
        print()
        print("🔐 Base64 encoded links:")
        print("   - L2dhbGxlcnkvbWF2ZXJpY2tzLXBob3Rvcy8= → /gallery/mavericks-photos/")
        print("   - L2dlYXIvd2V0c3VpdC1ndWlkZS8= → /gear/wetsuit-guide/")
        print("   - L2NvbmRpdGlvbnMvd2VhdGhlci1yZXBvcnRzLw== → /conditions/weather-reports/")
        print("   - L3Nwb3RzL3N1cmYtcmVwb3J0cy8= → /spots/surf-reports/")
        print("   - L3Nwb3RzL3RpZGUtcmVwb3J0cy8= → /spots/tide-reports/")
        print()
        print("Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    run_server() 