import http.server
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from services import *
import json
import re


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
        try:
            o = urlparse(self.path)
            uri = o.path.strip().split('/')
            if uri[1] == 'players' and len(uri) == 2:
                code, response = get_players()
                self.sendResponse(code, response)
            elif uri[1] == 'players' and len(uri) == 3:
                if not re.match('^[\d]+$', uri[2]):
                    self.sendResponse(400, 'Invalid id')
                else:
                    code, response = get_player(int(uri[2]))
                    self.sendResponse(code, response)
            elif uri[1] == 'games' and len(uri) == 2:
                code, response = get_games()
                self.sendResponse(code, response)
            elif uri[1] == 'games' and len(uri) == 3:
                if not re.match('^[\d]+$', uri[2]):
                    self.sendResponse(400, 'Invalid id')
                else:
                    code, response = get_game(int(uri[2]))
                    self.sendResponse(code, response)
            elif uri[1] == 'rules' and len(uri) == 2:
                code, response = get_rules()
                self.sendResponse(code, response)
            elif uri[1] == 'rules' and len(uri) == 3:
                if not re.match('^[\d]+$', uri[2]):
                    self.sendResponse(400, 'Invalid id')
                else:
                    code, response = get_rule(int(uri[2]))
                    self.sendResponse(code, response)
            elif uri[1] == 'games' and uri[3] == 'players' and len(uri) == 4:
                if not re.match('^[\d]+$', uri[2]):
                    self.sendResponse(400, 'Invalid id')
                else:
                    code, response = get_players_by_game(int(uri[2]))
                    self.sendResponse(code, response)
            elif uri[1] == 'games' and uri[3] == 'players' and len(uri) == 5:
                if not re.match('^[\d]+$', uri[2]) or not re.match('^[\d]+$', uri[4]):
                    self.sendResponse(400, 'Invalid id')
                else:
                    code, response = get_player_by_game(int(uri[2]), int(uri[4]))
                    self.sendResponse(code, response)
            elif uri[1] == 'games' and uri[3] == 'rules' and len(uri) == 4:
                if not re.match('^[\d]+$', uri[2]):
                    self.sendResponse(400, 'Invalid id')
                else:
                    code, response = get_rules_by_game(int(uri[2]))
                    self.sendResponse(code, response)
            elif uri[1] == 'games' and uri[3] == 'rules' and len(uri) == 5:
                if not re.match('^[\d]+$', uri[2]) or not re.match('^[\d]+$', uri[4]):
                    self.sendResponse(400, 'Invalid id')
                else:
                    code, response = get_rule_by_game(int(uri[2]), int(uri[4]))
                    self.sendResponse(code, response)
            else:
                self.sendResponse(404, {'message': 'Page not found'})
        except Exception as err:
            self.sendResponse(500, str(err))

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
                    elif uri[1] == 'games' and len(uri) == 2:
                        code, response = post_game(data)
                        self.sendResponse(code, response)
                    elif uri[1] == 'rules' and len(uri) == 2:
                        code, response = post_rule(data)
                        self.sendResponse(code, response)
                    else:
                        self.sendResponse(405, 'Method not allowed')
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
                    if uri[1] == 'players' and len(uri) == 3:
                        code, response = put_player(data, int(uri[2]))
                        self.sendResponse(code, response)
                    elif uri[1] == 'players' and len(uri) == 2:
                        self.sendResponse(405, 'Method not allowed')
                    elif uri[1] == 'games' and len(uri) == 3:
                        code, response = put_game(data, int(uri[2]))
                        self.sendResponse(code, response)
                    elif uri[1] == 'games' and len(uri) == 2:
                        self.sendResponse(405, 'Method not allowed')
                    elif uri[1] == 'rules' and len(uri) == 3:
                        code, response = put_rule(data, int(uri[2]))
                        self.sendResponse(code, response)
                    elif uri[1] == 'rules' and len(uri) == 2:
                        self.sendResponse(405, 'Method not allowed')
                    else:
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
                if uri[1] == 'players' and len(uri) == 3:
                    if not re.match('^[\d]+$', uri[2]):
                        self.sendResponse(400, 'Invalid id')
                    else:
                        code, response = delete_player(int(uri[2]))
                        self.sendResponse(code, response)
                elif uri[1] == 'players' and len(uri) == 2:
                    self.sendResponse(405, 'Method not allowed')
                elif uri[1] == 'games' and len(uri) == 2:
                    self.sendResponse(405, 'Method not allowed')
                elif uri[1] == 'games' and len(uri) == 3:
                    if not re.match('^[\d]+$', uri[2]):
                        self.sendResponse(400, 'Invalid id')
                    else:
                        code, response = delete_game(int(uri[2]))
                        self.sendResponse(code, response)
                elif uri[1] == 'rules' and len(uri) == 3:
                    if not re.match('^[\d]+$', uri[2]):
                        self.sendResponse(400, 'Invalid id')
                    else:
                        code, response = delete_rule(int(uri[2]))
                        self.sendResponse(code, response)
                elif uri[1] == 'rules' and len(uri) == 2:
                    self.sendResponse(405, 'Method not allowed')
                else:
                    self.sendResponse(405, 'Method not allowed')
        except Exception as err:
            self.sendResponse(500, str(err))


PORT = 9010
if __name__ == "__main__":
    handler = HttpHandler

    with HTTPServer(("", PORT), handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
