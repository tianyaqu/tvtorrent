#!/usr/bin/env python

import re
from pymongo import MongoClient
from basic import BaseHandler

class CategoryHandler(BaseHandler):
    #connect to mogodb
    def get(self):

        client = MongoClient()
        db = client['torrent']

        key = self.input('key',None)
        if key:
            pattern = re.compile(r'.*%s.*' %key,re.I)
            cursor_btList = db.priate.find({'name':pattern}) 
        else:
            cursor_btList = db.priate.find() 
        btList = []
        for i in cursor_btList:
            btList.append(i)
        total = len(btList) 

        curIndex = max(int(self.input('page',1)),1)
        itemsPerPage = 22 
        ybtList = btList[(curIndex-1)*itemsPerPage:curIndex*itemsPerPage]
        self.render(
            "category.html",
            title = "categoy header",
            btList = ybtList,
            total = total, 
            itemsPerPage = itemsPerPage, 
            curIndex = curIndex,
        )
