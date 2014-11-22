#!/usr/bin/env python

import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import re
import os.path
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
        )

        tornado.web.Application.__init__(self,handlers,**settings)
        #connect to mogodb
        self.db = None

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class HomeHandler(BaseHandler):
    def get(self):
        self.render(
            "index.html",
            title = "TV torrent | Home",
            text = "Welcome to TV torrent!",
        )

class CategoryHandler(BaseHandler):
    def get(self):
        self.render(
            "category.html",
            title = "category header",
            text = "hello caome",
        )

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(APP())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
