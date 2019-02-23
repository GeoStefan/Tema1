import http.server
import socketserver
from http.server import BaseHTTPRequestHandler

PORT = 8000

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text-html')
        self.end_headers()
        self.wfile.write("merge bine".encode())
        return

handler = HttpHandler

with socketserver.ThreadingTCPServer(("", PORT), handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()