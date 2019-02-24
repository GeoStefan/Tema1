import http.server
import socketserver
import json
import requests
from http.server import BaseHTTPRequestHandler
from urllib import parse
import datetime
import database
from log import Log

PORT = 8000



class HttpHandler(BaseHTTPRequestHandler):
    def getConfig(self):
        return json.load(open("config.json", "r"))

    def do_GET(self):
        db = database.Database()
        fullPath = self.path
        delimiter = fullPath.find("?")
        args = {}
        path = fullPath
        if delimiter != -1:
            args = parse.parse_qs(fullPath[delimiter + 1:])
            path = fullPath[:delimiter]

        if path == '/convert':
            url = "http://data.fixer.io/api/latest"
            key = self.getConfig()["api-key-convert"]
            queryParams = {"access_key": key, "symbols": "RON", "format": 1}
            result = requests.get(url, params=queryParams)

            if result.status_code == 200:
                rate = result.json()["rates"]["RON"]
                self.send_response(200)
                self.send_header('Content-type', 'text-html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"rate": rate}).encode())

                log = Log(1, str({"symbols": "RON", "format": 1}), result.content, result.elapsed.total_seconds(),
                          datetime.datetime.now())
                db.insertLogWs1(log)
            else:
                self.send_response(result.status_code)
                self.send_header('Content-type', 'text-html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(result.content)

                log = Log(0, str({"symbols": "RON", "format": 1}), result.content, result.elapsed.total_seconds(),
                          datetime.datetime.now())
                db.insertLogWs1(log)

        db.conn.close()
        return


if __name__ == "__main__":
    db = database.Database()
    db.createTables()
    db.conn.close()

    handler = HttpHandler

    with socketserver.ThreadingTCPServer(("", PORT), handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()