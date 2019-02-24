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
            print(result.content)

            if result.status_code == 200:
                rate = result.json()["rates"]["RON"]
                timestamp = result.json()["timestamp"]
                self.send_response(200)
                self.send_header('Content-type', 'text-html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"rate": rate,"timestamp": timestamp}).encode())

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

        if path.startswith("/rocket"):
            rocketId = path[path.rfind("/") + 1:]
            url = "https://api.spacexdata.com/v3/rockets/" + rocketId
            result = requests.get(url)
            print(result.content)

            if result.status_code == 200:
                cost = result.json()["cost_per_launch"]
                rocketName = result.json()["rocket_name"]
                self.send_response(200)
                self.send_header('Content-type', 'text-html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(result.json()).encode())

                log = Log(1, str({"rocketId": rocketId}), result.content, result.elapsed.total_seconds(),
                          datetime.datetime.now())
                db.insertLogWs2(log)
            else:
                self.send_response(result.status_code)
                self.send_header('Content-type', 'text-html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(result.content)

                log = Log(0, str({"rocketId": rocketId}), result.content, result.elapsed.total_seconds(),
                          datetime.datetime.now())
                db.insertLogWs2(log)

        db.conn.close()
        return

    def do_POST(self):
        db = database.Database()
        path = self.path
        len = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(len))

        if path == "/qr":
            url = "https://api.qrserver.com/v1/create-qr-code"
            queryParams = {"size": data["size"], "data": data["data"]}

            result = requests.get(url, params=queryParams)
            print(result.content)

            if result.status_code == 200:

                self.send_response(200)
                self.send_header('Content-type', 'text-html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'image/png')
                self.end_headers()
                self.wfile.write(result.content)

                log = Log(1, str({"size": data["size"], "data": data["data"]}), result.content,
                          result.elapsed.total_seconds(),
                          datetime.datetime.now())
                db.insertLogWs3(log)
            else:
                self.send_response(result.status_code)
                self.send_header('Content-type', 'text-html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(result.content)

                log = Log(0, str({"size": data["size"], "data": data["data"]}), result.content,
                          result.elapsed.total_seconds(),
                          datetime.datetime.now())
                db.insertLogWs3(log)

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
