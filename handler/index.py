#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web

from handler.base import BaseHandler


class IndexHandler(BaseHandler):

    def get(self, page=None):
        from lib.pager import Pager

        _p = int(page) if page else 1
        posts = self.post.get_posts(page=_p)
        pager = Pager(
            self.post.get_posts_count(), 10, _p, "/index/")
        self.render("index.html", posts=posts, pager=pager)


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


class PingHandler(BaseHandler):

    def get(self):
        self.write("Pong!")


class NotFoundHandler(BaseHandler):

    def get(self):
        self.render("404.html")
