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
            #(r"/categoryxstart=(\d+)",CategoryHandler),
        ]

        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__),"templates"),
            static_path = os.path.join(os.path.dirname(__file__),"static"),
            debug = True,
        )

        tornado.web.Application.__init__(self,handlers,**settings)

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def input(self,*args,**kwargs):
        return self.get_argument(*args,**kwargs)


class HomeHandler(BaseHandler):
    def get(self):
        self.render(
            "home.html",
            title = "TV torrent | Home",
            text = "Welcome to TV torrent!",
        )

class CategoryHandler(BaseHandler):
    #connect to mogodb
    client = MongoClient()
    db = client['torrent']
    cursor_btList = db.priate.find() 
    btList = []
    for i in cursor_btList:
        btList.append(i)
    total = len(btList) 
    def get(self):
        curIndex = max(int(self.input('start',1)),1)
        itemsPerPage = 22 
        ybtList = CategoryHandler.btList[(curIndex-1)*itemsPerPage:curIndex*itemsPerPage]
        self.render(
            "category.html",
            title = "categoy header",
            btList = ybtList,
            total = CategoryHandler.total, 
            itemsPerPage = itemsPerPage, 
            curIndex = curIndex,
        )

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(APP())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
