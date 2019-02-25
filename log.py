import json
import uuid


class Log:
    def __init__(self, status, request, response, latency, date):
        self.id = str(uuid.uuid4())
        self.status = status
        self.request = request
        self.response = response
        self.latency = latency
        self.date = date


class Metric:
    def __init__(self, passed, failed, avgLantency, minLantency, maxLantency):
        super().__init__()
        self.passed = passed
        self.failed = failed
        self.avgLatency = avgLantency
        self.minLatency = minLantency
        self.maxLatency = maxLantency


class Metrics:
    def __init__(self, convertM, rocketM, qrM):
        self.convert = convertM
        self.rocket = rocketM
        self.qr = qrM

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
