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

from handler.home import HomeHandler
from handler.category import CategoryHandler

define("port",default=8888,help="run on a given port",type=int)

class APP(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/",HomeHandler),
            (r"/category",CategoryHandler),
            (r"/search",CategoryHandler),
            #(r"/search",SearchHandler),
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

class SearchHandler(BaseHandler):
    def get(self):
        client = MongoClient()
        db = client['torrent']
        key = self.input('key','none')
        pattern = re.compile(r'.*%s.*' %key,re.I)
        cursor_btList = db.priate.find({'name':pattern}) 
        btList = []
        ybtList = []
        for i in cursor_btList:
            btList.append(i)
        total = len(btList) 
        itemsPerPage = 22 
        curIndex = 1
        ybtList = btList[0:curIndex*itemsPerPage]
        print total
        #print key
        self.render(
            "category.html",
            title = "Search Results",
            btList = ybtList,
            total = total, 
            itemsPerPage = 22, 
            curIndex = curIndex,
        )

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(APP())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
