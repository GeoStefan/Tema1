import http.server
import socketserver
import json
import requests
from http.server import BaseHTTPRequestHandler
from urllib import parse
import datetime
import base64
import database
from log import Log, Metrics

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
                converted = float(rate) * float(args["amount"][0])
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"rate": rate, "timestamp": timestamp, "converted": converted}).encode())

                log = Log(1, str({"symbols": "RON", "format": 1}), result.content, result.elapsed.total_seconds(),
                          datetime.datetime.now())
                try:
                    db.insertLogConvert(log)
                except:
                    print("Cannot insert in database")
            else:
                self.send_response(result.status_code)
                self.send_header('Content-type', 'text-html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(result.content)

                log = Log(0, str({"symbols": "RON", "format": 1}), result.content, result.elapsed.total_seconds(),
                          datetime.datetime.now())
                try:
                    db.insertLogConvert(log)
                except:
                    print("Cannot insert in database")

        if path.startswith("/rocket"):
            rocketId = path[path.rfind("/") + 1:]
            url = "https://api.spacexdata.com/v3/rockets/" + rocketId
            result = requests.get(url)
            print(result.content)

            if result.status_code == 200:
                r = result.json()
                rocket = {"rocketName": r["rocket_name"],
                          "costPerLaunch": r["cost_per_launch"],
                          "firstFlight": r["first_flight"],
                          "height": r["height"]["meters"],
                          "diameter": r["diameter"]["meters"],
                          "mass": r["mass"]["kg"],
                          "engines": r["engines"]["number"]}
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(rocket).encode())

                log = Log(1, str({"rocketId": rocketId}), result.content, result.elapsed.total_seconds(),
                          datetime.datetime.now())
                try:
                    db.insertLogRocket(log)
                except:
                    print("Cannot insert in database")
            else:
                self.send_response(result.status_code)
                self.send_header('Content-type', 'text-html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(result.content)

                log = Log(0, str({"rocketId": rocketId}), result.content, result.elapsed.total_seconds(),
                          datetime.datetime.now())
                try:
                    db.insertLogRocket(log)
                except:
                    print("Cannot insert in database")

        if path == "/metrics":
            metrics = Metrics(db.metricConvert(), db.metricRocket(), db.metricQr())

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(metrics.toJSON().encode())

        db.conn.close()
        return

    def do_POST(self):
        db = database.Database()
        path = self.path
        len = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(len))
        print(data)
        if path == "/qr":
            url = "https://api.qrserver.com/v1/create-qr-code"
            queryParams = {"size": data["size"], "data": data["data"]}

            result = requests.get(url, params=queryParams)
            print(result.content)

            if result.status_code == 200:

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(bytes(json.dumps({"qr": str(base64.b64encode(result.content))}), "utf-8"))

                log = Log(1, str({"size": data["size"], "data": data["data"]}), result.content,
                          result.elapsed.total_seconds(),
                          datetime.datetime.now())
                try:
                    db.insertLogQr(log)
                except:
                    print("Cannot insert in database")
            else:
                self.send_response(result.status_code)
                self.send_header('Content-type', 'text-html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(result.content)

                log = Log(0, str({"size": data["size"], "data": data["data"]}), result.content,
                          result.elapsed.total_seconds(),
                          datetime.datetime.now())
                try:
                    db.insertLogQr(log)
                except:
                    print("Cannot insert in database")

        db.conn.close()
        return

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.end_headers()
        return


if __name__ == "__main__":
    db = database.Database()
    db.createTables()
    db.conn.close()

    handler = HttpHandler

    with socketserver.ThreadingTCPServer(("", PORT), handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
