#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.web

from handler.base import BaseHandler
from config import feeds_dict


class SyncHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.rss_model.sync(feeds_dict)
        self.write("Done!")
