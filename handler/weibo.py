#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.web

from handler.base import BaseHandler


class SigninHandler(BaseHandler):

    def get(self):
        self.redirect(self.weibo_oauth.get_authorize_url(), permanent=False)


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

        exists_token = self.weibo_model.get_config("weibo")

        if exists_token and access_token.uid != exists_token["uid"]:
            self.raise_error(403)
            return

        self.weibo_model.replace_config(
            "weibo", {
                "access_token": access_token.access_token,
                "expires_in": access_token.expires_in,
                "uid": access_token.uid
            })

        self.signin(access_token.uid, "weibo")

        self.redirect("/", permanent=False)


class SyncHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        access_token = self.weibo_model.get_config("weibo")
        self.weibo_oauth.set_access_token(access_token)
        self.weibo_model.sync(self.weibo_oauth)
        self.write("Done!")
