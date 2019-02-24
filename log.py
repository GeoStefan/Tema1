import uuid


class Log:
    def __init__(self, status, request, response, latency, date):
        self.id = str(uuid.uuid4())
        self.status = status
        self.request = request
        self.response = response
        self.latency = latency
        self.date = date
