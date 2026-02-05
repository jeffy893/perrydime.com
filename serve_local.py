#!/usr/bin/env python3.10
"""
Simple HTTP server for local development of Perry Dime website.
Serves the docs/ folder on localhost:8000 with threading for better performance.
"""

import http.server
import socketserver
import os
from pathlib import Path

# Configuration
PORT = 8000
DIRECTORY = Path(__file__).parent / "docs"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)
    
    def end_headers(self):
        # Add cache control headers for development
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Expires', '0')
        super().end_headers()

def main():
    """Start the local development server with threading."""
    print("=" * 70)
    print("Perry Dime Local Development Server (Python 3.10)")
    print("=" * 70)
    print(f"\nServing directory: {DIRECTORY}")
    print(f"Server running at: http://localhost:{PORT}")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 70)
    print()
    
    # Use ThreadingTCPServer for concurrent request handling
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")

if __name__ == "__main__":
    main()

