#! /usr/bin/env python

import tornado.web

class BaseHandler(tornado.web.RequestHandler):
#    @property
    def input(self,*args,**kwargs):
        return self.get_argument(*args,**kwargs)
