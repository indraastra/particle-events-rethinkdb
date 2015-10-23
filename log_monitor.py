import json

import rethinkdb as r
import tornado
from tornado import ioloop, gen
from tornado.web import RequestHandler, Application, url

from config import *

@gen.coroutine
def insert_into(table, record):
    """
    Generic database record creator.
    """
    connection = yield r.connect(host=DB_HOST, port=28015)
    res = yield r.db(DB_NAME).table(table).insert(record).run(connection)
    print(table, record)
    return res["inserted"] == 1


class LogHandler(RequestHandler):
    """
    Handles creation of log records posted to /log.
    """
    def get(self):
        self.write("ok")

    @gen.coroutine
    def post(self):
        log = tornado.escape.json_decode(self.request.body)
        self.write("ok")
        yield insert_into(LOG_TABLE_NAME, log)



if __name__ == '__main__':
    print("Starting log monitor!")
    r.set_loop_type("tornado")
    app = Application([ url(r"/log", LogHandler) ])
    app.listen(MONITOR_PORT)
    ioloop.IOLoop.current().start()
