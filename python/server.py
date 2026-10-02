from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # Allow the browser to talk to us (CORS)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        if self.path == '/api/move':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            data = json.loads(body)

            direction = data.get('direction', 'stop')
            speed = data.get('speed', 0)
            a_pressed = data.get('a_pressed', False)

            print(f"Direction: {direction:8} | Speed: {speed:3}% | A pressed: {a_pressed}")

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Silence the default request logging
        pass

if __name__ == '__main__':
    print("Server running on http://localhost:5000")
    print("Press Ctrl+C to stop")
    HTTPServer(('0.0.0.0', 5000), Handler).serve_forever()