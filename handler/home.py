#! /usr/bin/env python

from basic import BaseHandler

class HomeHandler(BaseHandler):
    def get(self):
        self.render(
            "home.html",
            title = "Tv torrent | Home",
            text = "Welcome 2 TV torrent!",
        )
