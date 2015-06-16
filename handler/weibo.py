#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.web

from handler.base import BaseHandler


class SigninHandler(BaseHandler):

    def get(self):
        accounts = self.binded_accounts
        if not accounts or "weibo" in accounts:
            self.redirect(
                self.weibo_oauth.get_authorize_url(), permanent=False)
        else:
            self.write("bind your weibo account first!")
            return


class BindHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.redirect(
            self.weibo_oauth.get_authorize_url(), permanent=False)


class CallbackHandler(BaseHandler):

    def get(self):
        code = self.get_argument("code")

        access_token = None
        try:
            access_token = self.weibo_oauth.request_access_token(code)
        except Exception, e:
            print(e)
            self.write("Weibo Oauth Failed!")
            return

        exists_token = self.weibo.get_access_token()

        if exists_token and access_token.uid != exists_token["uid"]:
            self.raise_error(403)
            return

        self.weibo.save_access_token(access_token)

        self.signin(access_token.uid, "weibo")

        self.redirect("/", permanent=False)


class SyncHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        access_token = self.weibo.get_access_token()
        self.weibo_oauth.set_access_token(access_token)
        self.weibo.sync(self.weibo_oauth)
        self.write("Done!")
