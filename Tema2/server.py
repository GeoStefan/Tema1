import http.server
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from services import *
import json


class HttpHandler(BaseHTTPRequestHandler):

    def sendResponse(self, code, message=None):
        self.send_response(code)
        if code != 204:
            self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        if code != 204:
            self.wfile.write(json.dumps(message).encode())

    def do_GET(self):
        o = urlparse(self.path)
        print(o)
        uri = o.path.strip().split('/')
        print(uri)
        if uri[1] == 'players' and len(uri) == 2:
            players = get_players()
            self.sendResponse(200, players)
        elif uri[1] == 'player' and len(uri) == 3:
            player = get_player(int(uri[2]))
            if player != None:
                self.sendResponse(200, player)
            else:
                self.sendResponse(404, 'Player not found')
        elif uri[3] == 'progress' and len(uri) == 4:
            progress = get_progress(int(uri[2]))
            if progress != None:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(progress).encode())
            else:
                self.send_response(204)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
        elif uri[4] == 'achievements' and len(uri) == 5:
            achievements = get_achievements(int(uri[2]))
            if achievements != None:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(achievements).encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'message': 'Page not found'}).encode())
        elif uri[4] == 'achievement' and len(uri) == 6:
            achievement = get_achievement(int(uri[5]), int(uri[2]))
            if achievement != None:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(achievement).encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'message': 'Page not found'}).encode())
        else:
            self.sendResponse(404, {'message': 'Page not found'})

    def do_POST(self):
        try:
            o = urlparse(self.path)
            uri = o.path.strip().split('/')
            length = int(self.headers['Content-Length'])
            type = False
            if self.headers['Content-Type'] != 'application/json':
                self.sendResponse(415, 'Content type ' + self.headers['Content-type'] + ' not supported')
            else:
                try:
                    data = json.loads(self.rfile.read(length))
                    type = True
                except Exception as err:
                    self.sendResponse(415, 'Content type ' + self.headers['Content-type'] + ' not supported')
                if type:
                    if uri[1] == 'players' and len(uri) == 2:
                        code, response = post_player(data)
                        self.sendResponse(code, response)
        except Exception as err:
            self.sendResponse(500, str(err))

    def do_PUT(self):
        try:
            o = urlparse(self.path)
            uri = o.path.strip().split('/')
            length = int(self.headers['Content-Length'])
            type = False
            if self.headers['Content-Type'] != 'application/json':
                self.sendResponse(415, 'Content type ' + self.headers['Content-type'] + ' not supported')
            else:
                try:
                    data = json.loads(self.rfile.read(length))
                    type = True
                except Exception as err:
                    self.sendResponse(415, 'Content type ' + self.headers['Content-type'] + ' not supported')
                if type:
                    if uri[1] == 'player' and len(uri) == 3:
                        code, response = put_player(data)
                        self.sendResponse(code, response)
                    elif uri[1] == 'players' and len(uri) == 2:
                        self.sendResponse(405, 'Method not allowed')
        except Exception as err:
            self.sendResponse(500, str(err))

    def do_DELETE(self):
        try:
            o = urlparse(self.path)
            uri = o.path.strip().split('/')
            length = int(self.headers['Content-Length'])
            if length != 0:
                self.sendResponse(415, 'Content type ' + self.headers['Content-type'] + ' not supported')
            else:
                if uri[1] == 'player' and len(uri) == 3:
                    code, response = delete_player(int(uri[2]))
                    self.sendResponse(code, response)
                elif uri[1] == 'players' and len(uri) == 2:
                    self.sendResponse(405, 'Method not allowed')
        except Exception as err:
            self.sendResponse(500, str(err))


PORT = 9010
if __name__ == "__main__":
    handler = HttpHandler

    with http.server.ThreadingHTTPServer(("", PORT), handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
