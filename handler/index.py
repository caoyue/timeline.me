#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web

from handler.base import BaseHandler


class IndexHandler(BaseHandler):

    def get(self, page=None):
        from lib.pager import Pager

        _p = int(page) if page else 1
        pagesize = self.config.site["pagesize"]
        posts = self.posts.get_posts(page=_p, pagesize=pagesize)
        pager = Pager(
            self.posts.get_posts_count(), pagesize, _p, "/timeline/")
        self.render("index.html", posts=posts, pager=pager, cur="timeline")


class UserHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.write("signin type: %s <br/> uid: %s" %
                   (self.current_user["signin_type"], self.current_user["uid"]))


class SigninHandler(BaseHandler):

    def get(self):
        self.render("signin.html")


class SignoutHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.signout()
        self.redirect("/", permanent=False)


class AdminHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render("admin.html")


class PingHandler(BaseHandler):

    def get(self):
        self.write("pong!")


class NotFoundHandler(BaseHandler):

    def get(self):
        self.render("404.html")
