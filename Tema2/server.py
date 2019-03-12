import http.server
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
import Database
import json

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        o = urlparse(self.path)
        print(o)
        uri = o.path.strip().split('/')
        print(uri)
        if uri[1] == 'players':
            players = Database.select_players()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(players).encode())
        if uri[1] == 'player' and uri[2] != None:
            player = Database.select_player(int(uri[2]))
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(player).encode())

PORT = 9010
if __name__ == "__main__":

    handler = HttpHandler

    with http.server.ThreadingHTTPServer(("", PORT), handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
