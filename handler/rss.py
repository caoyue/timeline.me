#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.web

from handler.base import BaseHandler


class FeedHandler(BaseHandler):

    def get(self):
        posts = self.posts.get_posts(1, 20)
        self.set_header('Content-Type', 'text/xml')
        return self.render("feed.html", posts=posts, title="feed")


class SyncHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.rss.sync(self.config.feeds)
        self.write("Done!")
