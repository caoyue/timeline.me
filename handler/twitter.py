#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.web

from handler.base import BaseHandler


class SigninHandler(BaseHandler):

    def get(self):
        accounts = self.binded_accounts
        if not accounts or "twitter" in accounts:
            url = self.twitter_oauth.get_authorize_url()
            request_token = self.twitter_oauth.get_request_token()

            self.twitter.save_request_token(request_token)
            self.redirect(url, permanent=False)
        else:
            self.write("bind your twitter account first!")
            return


class BindHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        url = self.twitter_oauth.get_authorize_url()
        request_token = self.twitter_oauth.get_request_token()

        self.twitter.save_request_token(request_token)
        self.redirect(url, permanent=False)


class CallbackHandler(BaseHandler):

    def get(self):
        oauth_verifier = self.get_argument("oauth_verifier")

        access_token = None
        try:
            request_token = self.twitter.get_request_token()
            self.twitter_oauth.set_request_token(request_token)
            access_token = self.twitter_oauth.request_access_token(
                oauth_verifier)
        except Exception, e:
            self.write("Twitter Oauth Failed!")
            return

        exists_token = self.twitter.get_access_token()

        self.twitter_oauth.set_access_token(access_token)
        user_info = self.twitter_oauth.get_user_info()

        # admin only
        if exists_token and user_info["id"] != exists_token["uid"]:
            self.raise_error(403)
            return

        self.twitter.save_access_token(access_token, user_info["id"])

        self.signin(user_info["id"], "twitter")
        self.redirect("/", permanent=False)


class SyncHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        access_token = self.twitter.get_access_token()
        self.twitter_oauth.set_access_token(access_token)
        self.twitter.sync_all(self.twitter_oauth)
        self.write("Done!")
