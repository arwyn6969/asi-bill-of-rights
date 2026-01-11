#!/usr/bin/env python3
"""
Simple HTTP server to serve the Telegram Mini App locally.
Run this to test the Mini App before deploying.
"""

import http.server
import socketserver
import os

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Enable CORS for local testing
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🏠 KEVIN's Place Mini App Server")
        print(f"   Serving at: http://localhost:{PORT}/webapp.html")
        print(f"   Press Ctrl+C to stop")
        print()
        print("📱 To use with Telegram:")
        print("   1. Deploy this to a public HTTPS URL (ngrok, Cloudflare, etc)")
        print("   2. Set that URL as your bot's WebApp URL in @BotFather")
        print()
        httpd.serve_forever()
