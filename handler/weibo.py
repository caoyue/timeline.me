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

        user = None
        try:
            user = self.weibo_oauth.get_user_info({
                'code': code
            })

        except Exception as e:
            self.write("Weibo Oauth Failed: {0}".format(e))
            return

        exists_token = self.weibo.get_access_token()
        access_token = self.weibo_oauth.request_access_token()
        uid = str(user['uid'])

        if exists_token and uid != exists_token["uid"]:
            self.raise_error(403)
            return

        self.weibo.save_access_token(access_token, uid)

        self.signin(uid, "weibo")

        self.redirect("/", permanent=False)


class SyncHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        access_token = self.weibo.get_access_token()
        self.weibo_oauth.set_access_token(access_token)
        self.weibo.sync(self.weibo_oauth)
        self.write("Done!")
