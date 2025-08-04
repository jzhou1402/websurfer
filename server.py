#!/usr/bin/env python3
"""
Travel Blog HTTP server with realistic URLs and hidden test scenarios
"""

import http.server
import socketserver
import threading
import time
import os
from urllib.parse import urlparse, parse_qs

class TravelBlogHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        """Handle GET requests with special cases for testing"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        print(f"Request: {self.path}")
        
        # Handle hanging requests (disguised as real travel content)
        if path in ['/destinations/swiss-alps-hiking-guide', '/destinations/bali-hidden-beaches', 
                   '/destinations/ancient-rome-guide', '/destinations/bangkok-street-food',
                   '/travel-tips/planning-tools', '/photography/equipment-guide']:
            self.handle_hanging_request(path)
            return
        
        # Handle 404 errors (realistic missing content)
        if path in ['/destinations/japan', '/destinations/iceland', '/destinations/new-zealand',
                   '/destinations/morocco', '/destinations/peru', '/destinations/australia',
                   '/destinations/croatia', '/destinations/portugal', '/category/adventure',
                   '/category/culture', '/category/food', '/category/budget', '/category/luxury',
                   '/category/solo', '/category/family', '/category/road-trip',
                   '/services/travel-insurance', '/services/visa-assistance', '/services/booking-support',
                   '/services/travel-consultation', '/services/photography-workshops', '/services/guided-tours',
                   '/newsletter', '/instagram', '/youtube', '/facebook', '/twitter', '/pinterest',
                   '/privacy-policy', '/terms-of-service', '/sitemap', '/advertising', '/partnerships']:
            self.send_404_error(path)
            return
        
        # Handle working pages
        if path == '/destinations':
            self.send_destinations_page()
            return
        elif path == '/travel-tips':
            self.send_travel_tips_page()
            return
        elif path == '/photography':
            self.send_photography_page()
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
        """Handle requests that should hang/never respond (disguised as travel content)"""
        print(f"Hanging request detected: {path}")
        
        # Different hanging behaviors based on the path
        if path == '/destinations/swiss-alps-hiking-guide':
            # Hangs forever (like a slow loading page)
            while True:
                time.sleep(1)
        elif path == '/destinations/bali-hidden-beaches':
            # Very long delay (30 seconds)
            time.sleep(30)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Bali Hidden Beaches Guide</h1><p>Finally loaded after 30 seconds!</p>")
        elif path == '/destinations/ancient-rome-guide':
            # Infinite loop
            while True:
                pass
        elif path == '/destinations/bangkok-street-food':
            # Slow response (10 seconds)
            time.sleep(10)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Bangkok Street Food Guide</h1><p>Slow response after 10 seconds</p>")
        elif path == '/travel-tips/planning-tools':
            # 60 second delay
            time.sleep(60)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Travel Planning Tools</h1><p>Blocked request finally responded</p>")
        elif path == '/photography/equipment-guide':
            # 45 second delay
            time.sleep(45)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Photography Equipment Guide</h1><p>Long loading time completed</p>")
    
    def send_404_error(self, path):
        """Send a 404 error response with travel-themed styling"""
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Page Not Found - Wanderlust Adventures</title>
            <style>
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
                    color: #667eea; 
                    text-decoration: none;
                    font-weight: 500;
                    padding: 0.5rem 1rem;
                    border: 2px solid #667eea;
                    border-radius: 5px;
                    transition: all 0.3s;
                }}
                a:hover {{
                    background: #667eea;
                    color: white;
                }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <div class="error">404</div>
                <div class="message">Destination Not Found</div>
                <div class="path">Requested path: {path}</div>
                <p style="color: #666; margin: 1rem 0;">This travel destination seems to be off the beaten path.</p>
                <a href="/">← Back to Home</a>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode())
    
    def send_destinations_page(self):
        """Send destinations page"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Destinations - Wanderlust Adventures</title>
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
                h1 { color: #333; text-align: center; }
                .destinations-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 2rem;
                    margin-top: 2rem;
                }
                .destination-card {
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 1.5rem;
                    transition: transform 0.3s;
                }
                .destination-card:hover {
                    transform: translateY(-5px);
                }
                a { color: #667eea; text-decoration: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🌍 Explore Our Destinations</h1>
                <div class="destinations-grid">
                    <div class="destination-card">
                        <h3>🏔️ Swiss Alps</h3>
                        <p>Discover breathtaking mountain trails and alpine adventures.</p>
                        <a href="/destinations/swiss-alps-hiking-guide">Read Guide →</a>
                    </div>
                    <div class="destination-card">
                        <h3>🏖️ Bali</h3>
                        <p>Explore hidden beaches and tropical paradise.</p>
                        <a href="/destinations/bali-hidden-beaches">Discover Beaches →</a>
                    </div>
                    <div class="destination-card">
                        <h3>🏛️ Rome</h3>
                        <p>Step back in time to ancient Roman civilization.</p>
                        <a href="/destinations/ancient-rome-guide">Explore History →</a>
                    </div>
                    <div class="destination-card">
                        <h3>🍜 Bangkok</h3>
                        <p>Experience the vibrant street food culture.</p>
                        <a href="/destinations/bangkok-street-food">Food Tour →</a>
                    </div>
                </div>
                <p style="text-align: center; margin-top: 2rem;">
                    <a href="/" style="padding: 0.5rem 1rem; border: 2px solid #667eea; border-radius: 5px;">← Back to Home</a>
                </p>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode())
    
    def send_travel_tips_page(self):
        """Send travel tips page"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Travel Tips - Wanderlust Adventures</title>
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
                h1 { color: #333; text-align: center; }
                .tip-card {
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 1.5rem;
                    margin: 1rem 0;
                }
                a { color: #667eea; text-decoration: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>💡 Travel Tips & Resources</h1>
                <div class="tip-card">
                    <h3>Essential Planning Tools</h3>
                    <p>Make your next trip planning easier with these essential tools and resources.</p>
                    <a href="/travel-tips/planning-tools">View Resources →</a>
                </div>
                <p style="text-align: center; margin-top: 2rem;">
                    <a href="/" style="padding: 0.5rem 1rem; border: 2px solid #667eea; border-radius: 5px;">← Back to Home</a>
                </p>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode())
    
    def send_photography_page(self):
        """Send photography page"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Photography - Wanderlust Adventures</title>
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
                h1 { color: #333; text-align: center; }
                .photo-card {
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 1.5rem;
                    margin: 1rem 0;
                }
                a { color: #667eea; text-decoration: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📸 Photography Guide</h1>
                <div class="photo-card">
                    <h3>Equipment Guide</h3>
                    <p>Capture your travel memories with the right photography gear and techniques.</p>
                    <a href="/photography/equipment-guide">Learn More →</a>
                </div>
                <p style="text-align: center; margin-top: 2rem;">
                    <a href="/" style="padding: 0.5rem 1rem; border: 2px solid #667eea; border-radius: 5px;">← Back to Home</a>
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
            <title>About - Wanderlust Adventures</title>
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
                h1 { color: #333; text-align: center; }
                .content { background: #f8f9fa; border-radius: 10px; padding: 1.5rem; }
                a { color: #667eea; text-decoration: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>About Wanderlust Adventures</h1>
                <div class="content">
                    <p>We are passionate travelers sharing our adventures and insights from around the world. Our mission is to inspire others to explore, discover, and create unforgettable memories.</p>
                    <p>From hidden beaches to mountain peaks, from street food to fine dining, we document it all to help you plan your next adventure.</p>
                </div>
                <p style="text-align: center; margin-top: 2rem;">
                    <a href="/" style="padding: 0.5rem 1rem; border: 2px solid #667eea; border-radius: 5px;">← Back to Home</a>
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
            <title>Contact - Wanderlust Adventures</title>
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
                h1 { color: #333; text-align: center; }
                .content { background: #f8f9fa; border-radius: 10px; padding: 1.5rem; }
                a { color: #667eea; text-decoration: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Contact Us</h1>
                <div class="content">
                    <p>Get in touch with us for collaborations, questions, or just to share your travel stories!</p>
                    <p><strong>Email:</strong> hello@wanderlustadventures.com</p>
                    <p><strong>Follow us:</strong> @wanderlustadventures</p>
                </div>
                <p style="text-align: center; margin-top: 2rem;">
                    <a href="/" style="padding: 0.5rem 1rem; border: 2px solid #667eea; border-radius: 5px;">← Back to Home</a>
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
    
    with socketserver.TCPServer((host, port), TravelBlogHTTPRequestHandler) as httpd:
        print(f"🚀 Travel Blog Server started at http://localhost:{port}")
        if host == '0.0.0.0':
            print(f"🌐 Server is accessible from external connections")
        print(f"📁 Serving files from: {os.getcwd()}")
        print("🔗 Test the following:")
        print("   - Working pages: /, /destinations, /travel-tips, /photography, /about, /contact")
        print("   - 404 errors: /destinations/japan, /category/adventure, /services/travel-insurance")
        print("   - Hanging requests: /destinations/swiss-alps-hiking-guide, /travel-tips/planning-tools")
        print("\n⏹️  Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    run_server() 