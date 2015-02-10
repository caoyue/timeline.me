#!/usr/bin/env python
# -*- coding: utf-8 -*-


from handler.base import BaseHandler


class IndexHandler(BaseHandler):

    def get(self):
        self.write("Hello!")


class SignoutHandler(BaseHandler):

    def get(self):
        self.signout()
        self.redirect("/", permanent=False)


class TestHandler(BaseHandler):

    def get(self):
        self.write("Done!")
