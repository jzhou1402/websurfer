#!/usr/bin/env python3
"""
NorCal Surf Adventures HTTP server with realistic surf URLs and hidden test scenarios
"""

import http.server
import socketserver
import threading
import time
import os
from urllib.parse import urlparse, parse_qs

class SurfAdventuresHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        """Handle GET requests with special cases for testing"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        print(f"Request: {self.path}")
        
        # Handle hanging requests (disguised as surf spot guides)
        if path in ['/spots/mavericks', '/spots/steamer-lane', '/spots/stinson-beach', 
                   '/spots/fort-point', '/gear/equipment-guide', '/conditions/reports']:
            self.handle_hanging_request(path)
            return
        
        # Handle 404 errors (realistic missing surf content)
        if path in ['/spots/pleasure-point', '/spots/rockaway', '/spots/ob', '/spots/linda-mar',
                   '/category/big-wave', '/category/point-breaks', '/category/beach-breaks',
                   '/category/reef-breaks', '/category/beginner-friendly', '/category/advanced',
                   '/category/winter-spots', '/category/summer-spots',
                   '/services/surf-lessons', '/services/board-rental', '/services/wetsuit-rental',
                   '/services/surf-guides', '/services/safety-courses', '/services/competitions',
                   '/newsletter', '/instagram', '/youtube', '/facebook', '/twitter', '/surfline',
                   '/privacy-policy', '/terms-of-service', '/sitemap', '/advertising', '/partnerships']:
            self.send_404_error(path)
            return
        
        # Handle working pages
        if path == '/spots':
            self.send_spots_page()
            return
        elif path == '/conditions':
            self.send_conditions_page()
            return
        elif path == '/gear':
            self.send_gear_page()
            return
        elif path == '/about':
            self.send_about_page()
            return
        elif path == '/contact':
            self.send_contact_page()
            return
        
        # Default: serve index.html for root or serve static files
        if path == '/' or path == '/index.html':
            self.serve_file('index.html')
        else:
            # Try to serve as static file, fallback to 404
            if os.path.exists(path[1:]):  # Remove leading slash
                super().do_GET()
            else:
                self.send_404_error(path)
    
    def handle_hanging_request(self, path):
        """Handle requests that should hang/never respond (disguised as surf content)"""
        print(f"Hanging request detected: {path}")
        
        # Different hanging behaviors based on the path
        if path == '/spots/mavericks':
            # Hangs forever (like a big wave that never comes)
            while True:
                time.sleep(1)
        elif path == '/spots/steamer-lane':
            # Very long delay (30 seconds)
            time.sleep(30)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Steamer Lane Guide</h1><p>Finally loaded after 30 seconds!</p>")
        elif path == '/spots/stinson-beach':
            # Infinite loop
            while True:
                pass
        elif path == '/spots/fort-point':
            # Slow response (10 seconds)
            time.sleep(10)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Fort Point Guide</h1><p>Slow response after 10 seconds</p>")
        elif path == '/gear/equipment-guide':
            # 60 second delay
            time.sleep(60)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Surf Equipment Guide</h1><p>Blocked request finally responded</p>")
        elif path == '/conditions/reports':
            # 45 second delay
            time.sleep(45)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Surf Conditions Report</h1><p>Long loading time completed</p>")
    
    def send_404_error(self, path):
        """Send a 404 error response with surf-themed styling"""
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Spot Not Found - NorCal Surf Adventures</title>
            <style>
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #74b9ff 100%);
                    margin: 0;
                    padding: 0;
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                .error-container {{
                    background: white;
                    border-radius: 15px;
                    padding: 3rem;
                    text-align: center;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                    max-width: 500px;
                }}
                .error {{ 
                    color: #d32f2f; 
                    font-size: 4rem; 
                    margin-bottom: 1rem; 
                }}
                .message {{ 
                    font-size: 1.5rem; 
                    margin-bottom: 1rem;
                    color: #333;
                }}
                .path {{ 
                    background: #f5f5f5; 
                    padding: 1rem; 
                    border-radius: 5px; 
                    font-family: monospace;
                    margin: 1rem 0;
                    color: #666;
                }}
                a {{ 
                    color: #1e3c72; 
                    text-decoration: none;
                    font-weight: 500;
                    padding: 0.5rem 1rem;
                    border: 2px solid #1e3c72;
                    border-radius: 5px;
                    transition: all 0.3s;
                }}
                a:hover {{
                    background: #1e3c72;
                    color: white;
                }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <div class="error">404</div>
                <div class="message">Surf Spot Not Found</div>
                <div class="path">Requested path: {path}</div>
                <p style="color: #666; margin: 1rem 0;">This surf spot seems to be off the radar.</p>
                <a href="/">← Back to Home</a>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode())
    
    def send_spots_page(self):
        """Send surf spots page"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Surf Spots - NorCal Surf Adventures</title>
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #74b9ff 100%);
                    margin: 0;
                    padding: 2rem;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    padding: 2rem;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                }
                h1 { color: #1e3c72; text-align: center; }
                .spots-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 2rem;
                    margin-top: 2rem;
                }
                .spot-card {
                    background: linear-gradient(135deg, #f8f9fa 0%, #e3f2fd 100%);
                    border-radius: 10px;
                    padding: 1.5rem;
                    transition: transform 0.3s;
                    border-left: 4px solid #74b9ff;
                }
                .spot-card:hover {
                    transform: translateY(-5px);
                }
                a { color: #1e3c72; text-decoration: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🌊 NorCal Surf Spots</h1>
                <div class="spots-grid">
                    <div class="spot-card">
                        <h3>🏄‍♂️ Mavericks</h3>
                        <p>The legendary big wave spot off Half Moon Bay.</p>
                        <a href="/spots/mavericks">Read Guide →</a>
                    </div>
                    <div class="spot-card">
                        <h3>🏄‍♀️ Steamer Lane</h3>
                        <p>Santa Cruz's famous right-hand point break.</p>
                        <a href="/spots/steamer-lane">Read Guide →</a>
                    </div>
                    <div class="spot-card">
                        <h3>🏖️ Stinson Beach</h3>
                        <p>Family-friendly beach break in Marin County.</p>
                        <a href="/spots/stinson-beach">Read Guide →</a>
                    </div>
                    <div class="spot-card">
                        <h3>🏰 Fort Point</h3>
                        <p>Urban surfing under the Golden Gate Bridge.</p>
                        <a href="/spots/fort-point">Read Guide →</a>
                    </div>
                </div>
                <p style="text-align: center; margin-top: 2rem;">
                    <a href="/" style="padding: 0.5rem 1rem; border: 2px solid #1e3c72; border-radius: 5px;">← Back to Home</a>
                </p>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode())
    
    def send_conditions_page(self):
        """Send conditions page"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Surf Conditions - NorCal Surf Adventures</title>
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #74b9ff 100%);
                    margin: 0;
                    padding: 2rem;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    padding: 2rem;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                }
                h1 { color: #1e3c72; text-align: center; }
                .condition-card {
                    background: linear-gradient(135deg, #f8f9fa 0%, #e3f2fd 100%);
                    border-radius: 10px;
                    padding: 1.5rem;
                    margin: 1rem 0;
                    border-left: 4px solid #74b9ff;
                }
                a { color: #1e3c72; text-decoration: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🌊 Surf Conditions</h1>
                <div class="condition-card">
                    <h3>Real-time Reports</h3>
                    <p>Get the latest conditions for all NorCal surf spots.</p>
                    <a href="/conditions/reports">Check Reports →</a>
                </div>
                <p style="text-align: center; margin-top: 2rem;">
                    <a href="/" style="padding: 0.5rem 1rem; border: 2px solid #1e3c72; border-radius: 5px;">← Back to Home</a>
                </p>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode())
    
    def send_gear_page(self):
        """Send gear page"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Surf Gear - NorCal Surf Adventures</title>
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #74b9ff 100%);
                    margin: 0;
                    padding: 2rem;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    padding: 2rem;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                }
                h1 { color: #1e3c72; text-align: center; }
                .gear-card {
                    background: linear-gradient(135deg, #f8f9fa 0%, #e3f2fd 100%);
                    border-radius: 10px;
                    padding: 1.5rem;
                    margin: 1rem 0;
                    border-left: 4px solid #74b9ff;
                }
                a { color: #1e3c72; text-decoration: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏄‍♂️ Surf Gear Guide</h1>
                <div class="gear-card">
                    <h3>Equipment Guide</h3>
                    <p>Get the right equipment for NorCal's challenging conditions.</p>
                    <a href="/gear/equipment-guide">View Guide →</a>
                </div>
                <p style="text-align: center; margin-top: 2rem;">
                    <a href="/" style="padding: 0.5rem 1rem; border: 2px solid #1e3c72; border-radius: 5px;">← Back to Home</a>
                </p>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode())
    
    def send_about_page(self):
        """Send about page"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>About - NorCal Surf Adventures</title>
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #74b9ff 100%);
                    margin: 0;
                    padding: 2rem;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    padding: 2rem;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                }
                h1 { color: #1e3c72; text-align: center; }
                .content { background: linear-gradient(135deg, #f8f9fa 0%, #e3f2fd 100%); border-radius: 10px; padding: 1.5rem; border-left: 4px solid #74b9ff; }
                a { color: #1e3c72; text-decoration: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>About NorCal Surf Adventures</h1>
                <div class="content">
                    <p>We are passionate surfers sharing our knowledge of Northern California's legendary surf spots. Our mission is to help surfers of all levels discover and safely enjoy the incredible waves along the NorCal coastline.</p>
                    <p>From the massive waves of Mavericks to the family-friendly breaks of Stinson Beach, we provide comprehensive guides and real-time information to enhance your surfing experience.</p>
                </div>
                <p style="text-align: center; margin-top: 2rem;">
                    <a href="/" style="padding: 0.5rem 1rem; border: 2px solid #1e3c72; border-radius: 5px;">← Back to Home</a>
                </p>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode())
    
    def send_contact_page(self):
        """Send contact page"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Contact - NorCal Surf Adventures</title>
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #74b9ff 100%);
                    margin: 0;
                    padding: 2rem;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    padding: 2rem;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                }
                h1 { color: #1e3c72; text-align: center; }
                .content { background: linear-gradient(135deg, #f8f9fa 0%, #e3f2fd 100%); border-radius: 10px; padding: 1.5rem; border-left: 4px solid #74b9ff; }
                a { color: #1e3c72; text-decoration: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Contact Us</h1>
                <div class="content">
                    <p>Get in touch with us for surf reports, gear recommendations, or just to share your NorCal surf stories!</p>
                    <p><strong>Email:</strong> hello@norcalsurfadventures.com</p>
                    <p><strong>Follow us:</strong> @norcalsurfadventures</p>
                </div>
                <p style="text-align: center; margin-top: 2rem;">
                    <a href="/" style="padding: 0.5rem 1rem; border: 2px solid #1e3c72; border-radius: 5px;">← Back to Home</a>
                </p>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode())
    
    def serve_file(self, filename):
        """Serve a static file"""
        try:
            with open(filename, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_404_error(filename)

def run_server(port=None):
    """Run the HTTP server"""
    # Get port from environment variable (for cloud hosting) or use default
    if port is None:
        port = int(os.environ.get('PORT', 8000))
    
    # Bind to all interfaces for cloud hosting
    host = '0.0.0.0'
    
    with socketserver.TCPServer((host, port), SurfAdventuresHTTPRequestHandler) as httpd:
        print(f"🌊 NorCal Surf Adventures Server started at http://localhost:{port}")
        if host == '0.0.0.0':
            print(f"🌐 Server is accessible from external connections")
        print(f"📁 Serving files from: {os.getcwd()}")
        print("🔗 Test the following:")
        print("   - Working pages: /, /spots, /conditions, /gear, /about, /contact")
        print("   - 404 errors: /spots/pleasure-point, /category/big-wave, /services/surf-lessons")
        print("   - Hanging requests: /spots/mavericks, /spots/steamer-lane, /gear/equipment-guide")
        print("\n⏹️  Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    run_server() 