from http.server import BaseHTTPRequestHandler
import json
import os
import sys

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "status": "ok",
            "version": "32.0-HTTP-BASELINE",
            "message": "Raw HTTP Handler is LIVE",
            "python_version": sys.version,
            "cwd": os.getcwd(),
            "path": self.path
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return
