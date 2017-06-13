#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import tornado.web

from handler.base import BaseHandler


class SigninHandler(BaseHandler):

    def get(self):
        accounts = self.binded_accounts
        if not accounts or "twitter" in accounts:
            url = self.twitter_oauth.get_authorize_url()
            self.set_secure_cookie("_token", json.dumps(
                self.twitter_oauth.get_request_token()))
            self.redirect(url, permanent=False)
        else:
            self.write("bind your twitter account first!")
            return


class BindHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        url = self.twitter_oauth.get_authorize_url()
        self.redirect(url, permanent=False)


class CallbackHandler(BaseHandler):

    def get(self):
        oauth_verifier = self.get_argument("oauth_verifier")

        user = None
        try:
            request_token = json.loads(self.get_secure_cookie("_token"))
            user = self.twitter_oauth.get_user_info({
                'oauth_verifier': oauth_verifier
            }, request_token)
            self.application.data['request_token'] = {}
        except Exception as e:
            self.write("Twitter Oauth Failed: {0}".format(e))
            return

        exists_token = self.twitter.get_access_token()
        access_token = self.twitter_oauth.request_access_token()
        uid = str(user['uid'])

        # admin only
        if exists_token and uid != str(exists_token["uid"]):
            self.raise_error(403)
            return

        self.twitter.save_access_token(access_token, uid)

        self.signin(uid, "twitter")
        self.redirect("/", permanent=False)


class SyncHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        access_token = self.twitter.get_access_token()
        self.twitter_oauth.set_access_token(access_token)
        self.twitter.sync(self.twitter_oauth)
        self.write("Done!")
