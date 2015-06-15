#!/usr/bin/env python
# -*- coding: utf-8 -*-


from handler.base import BaseHandler


class IndexHandler(BaseHandler):

    def get(self, page=None):
        from lib.pager import Pager

        _p = int(page) if page else 1
        pagesize = self.config.site["pagesize"]
        posts = self.posts.get_posts(
            page=_p, pagesize=pagesize, source="INDEX")
        pager = Pager(
            self.posts.get_posts_count(source="INDEX"), pagesize, _p, "/timeline/")
        self.render("index.html", posts=posts, pager=pager, cur="timeline")


class PingHandler(BaseHandler):

    def get(self):
        self.write("pong!")


class NotFoundHandler(BaseHandler):

    def get(self):
        self.render("404.html")
