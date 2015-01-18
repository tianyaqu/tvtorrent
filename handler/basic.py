#! /usr/bin/env python

import tornado.web

class BaseHandler(tornado.web.RequestHandler):
#    @property
    def input(self,*args,**kwargs):
        return self.get_argument(*args,**kwargs)

    def merge_query(self,args,mask = []):
        for k in self.request.arguments.keys():
            if k not in args:
                args[k] = self.get_argument(k)
        for k in mask:
            if k in args:
                del args[k]

        return args

    def makeurl(self,args,base = None):
        if base == None:
            base = self.request.path
        return tornado.httputil.url_concat(base,args)
