import sqlite3
from log import Metric


class Database:

    def __init__(self):
        self.conn = sqlite3.connect("metrici.db")
        self.c = self.conn.cursor()

    def createTables(self):
        self.c.execute(
            "CREATE TABLE if not exists LOG_CONVERT(id TEXT, status INTEGER , request TEXT, response TEXT, latency INTEGER, date DATE)")
        self.c.execute(
            "CREATE TABLE if not exists LOG_ROCKET(id TEXT, status INTEGER , request TEXT, response TEXT, latency INTEGER, date DATE)")
        self.c.execute(
            "CREATE TABLE if not exists LOG_QR(id TEXT, status INTEGER , request TEXT, response TEXT, latency INTEGER, date DATE)")

    def insertLogConvert(self, log):
        self.c.execute("INSERT INTO LOG_CONVERT VALUES (?,?,?,?,?,?)",
                       (log.id, log.status, log.request, log.response, log.latency, log.date))
        self.conn.commit()

    def insertLogRocket(self, log):
        self.c.execute("INSERT INTO LOG_ROCKET VALUES (?,?,?,?,?,?)",
                       (log.id, log.status, log.request, log.response, log.latency, log.date))
        self.conn.commit()

    def insertLogQr(self, log):
        self.c.execute("INSERT INTO LOG_QR VALUES (?,?,?,?,?,?)",
                       (log.id, log.status, log.request, log.response, log.latency, log.date))
        self.conn.commit()

    def metricConvert(self):
        self.c.execute("SELECT COUNT(*) FROM LOG_CONVERT WHERE status= 1")
        passed = self.c.fetchone()[0]

        self.c.execute("SELECT COUNT(*) FROM LOG_CONVERT WHERE status= 0")
        failed = self.c.fetchone()[0]

        self.c.execute("SELECT AVG(latency) FROM LOG_CONVERT")
        avgLantency = self.c.fetchone()[0]

        self.c.execute("SELECT MIN(latency) FROM LOG_CONVERT")
        minLantency = self.c.fetchone()[0]

        self.c.execute("SELECT MAX(latency) FROM LOG_CONVERT")
        maxLantency = self.c.fetchone()[0]

        return Metric(passed, failed, avgLantency, minLantency, maxLantency)

    def metricRocket(self):
        self.c.execute("SELECT COUNT(*) FROM LOG_ROCKET WHERE status= 1")
        passed = self.c.fetchone()[0]

        self.c.execute("SELECT COUNT(*) FROM LOG_ROCKET WHERE status= 0")
        failed = self.c.fetchone()[0]

        self.c.execute("SELECT AVG(latency) FROM LOG_ROCKET")
        avgLantency = self.c.fetchone()[0]

        self.c.execute("SELECT MIN(latency) FROM LOG_ROCKET")
        minLantency = self.c.fetchone()[0]

        self.c.execute("SELECT MAX(latency) FROM LOG_ROCKET")
        maxLantency = self.c.fetchone()[0]

        return Metric(passed, failed, avgLantency, minLantency, maxLantency)

    def metricQr(self):
        self.c.execute("SELECT COUNT(*) FROM LOG_QR WHERE status= 1")
        passed = self.c.fetchone()[0]

        self.c.execute("SELECT COUNT(*) FROM LOG_QR WHERE status= 0")
        failed = self.c.fetchone()[0]

        self.c.execute("SELECT AVG(latency) FROM LOG_QR")
        avgLantency = self.c.fetchone()[0]

        self.c.execute("SELECT MIN(latency) FROM LOG_QR")
        minLantency = self.c.fetchone()[0]

        self.c.execute("SELECT MAX(latency) FROM LOG_QR")
        maxLantency = self.c.fetchone()[0]

        return Metric(passed, failed, avgLantency, minLantency, maxLantency)


if __name__ == "__main__":
    db = Database()
    print(db.metricConvert())
    print(db.metricRocket())
    print(db.metricQr())
