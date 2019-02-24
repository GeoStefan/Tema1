import sqlite3


class Database:

    def __init__(self):
        self.conn = sqlite3.connect("metrici.db")
        self.c = self.conn.cursor()

    def createTables(self):
        self.c.execute(
            "CREATE TABLE if not exists LOGWS1(id TEXT, status INTEGER , request TEXT, response TEXT, latency INTEGER, date DATE)")
        self.c.execute(
            "CREATE TABLE if not exists LOGWS2(id TEXT, status INTEGER , request TEXT, response TEXT, latency INTEGER, date DATE)")
        self.c.execute(
            "CREATE TABLE if not exists LOGWS3(id TEXT, status INTEGER , request TEXT, response TEXT, latency INTEGER, date DATE)")

    def insertLogWs1(self, log):
        self.c.execute("INSERT INTO LOGWS1 VALUES (?,?,?,?,?,?)",
                       (log.id, log.status, log.request, log.response, log.latency, log.date))
        self.conn.commit()

    def insertLogWs2(self, log):
        self.c.execute("INSERT INTO LOGWS2 VALUES (?,?,?,?,?,?)",
                       (log.id, log.status, log.request, log.response, log.latency, log.date))
        self.conn.commit()

    def insertLogWs3(self, log):
        self.c.execute("INSERT INTO LOGWS3 VALUES (?,?,?,?,?,?)",
                       (log.id, log.status, log.request, log.response, log.latency, log.date))
        self.conn.commit()
