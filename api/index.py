from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        import json
        self.wfile.write(json.dumps({"status": "ok", "message": "Standard Library Python is working"}).encode('utf-8'))
        return
