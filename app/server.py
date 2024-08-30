import http.server
import socketserver

PORT = 8081  # You can change this to any port you prefer

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        # Handle OPTIONS requests to comply with CORS preflight requests
        self.send_response(200)
        self.end_headers()

Handler = CORSRequestHandler

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"Serving HTTP on 0.0.0.0 port {PORT} (http://0.0.0.0:{PORT}/) ...")
    httpd.serve_forever()
