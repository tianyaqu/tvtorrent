#!/usr/bin/env python

import re
import os.path
from pymongo import MongoClient
import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define,options

define("port",default=8888,help="run on a given port",type=int)

class APP(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/",HomeHandler),
            (r"/category",CategoryHandler),
        ]

        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__),"templates"),
            static_path = os.path.join(os.path.dirname(__file__),"static"),
            debug = True,
        )

        tornado.web.Application.__init__(self,handlers,**settings)
        #connect to mogodb
        client = MongoClient()
        self.db = client['torrent']

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class HomeHandler(BaseHandler):
    def get(self):
        self.render(
            "home.html",
            title = "TV torrent | Home",
            text = "Welcome to TV torrent!",
        )

class CategoryHandler(BaseHandler):
    def get(self):
        btList = self.db.priate.find() 
        xbtList = []
        for i in btList:
            xbtList.append(i)
        ybtList = xbtList[:20]
        self.render(
            "category.html",
            title = "category header",
            text = "hello caome",
            btList = ybtList,
        )

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(APP())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
