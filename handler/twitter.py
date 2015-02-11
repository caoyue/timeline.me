#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.web

from handler.base import BaseHandler


class SigninHandler(BaseHandler):

    def get(self):
        url = self.twitter_oauth.get_authorize_url()
        request_token = self.twitter_oauth.get_request_token()

        self.twitter.replace_config(
            "twitter_request_token", {
                "oauth_token": request_token["oauth_token"],
                "oauth_token_secret": request_token["oauth_token_secret"]
            })
        self.redirect(url, permanent=False)


class CallbackHandler(BaseHandler):

    def get(self):
        oauth_verifier = self.get_argument("oauth_verifier")

        access_token = None
        try:
            request_token = self.twitter.get_config(
                "twitter_request_token")
            self.twitter_oauth.set_request_token(request_token)
            access_token = self.twitter_oauth.request_access_token(
                oauth_verifier)
        except Exception, e:
            self.write("Twitter Oauth Failed!")
            return

        exists_token = self.twitter.get_config("twitter")

        self.twitter_oauth.set_access_token(access_token)
        user_info = self.twitter_oauth.get_user_info()

        # admin only
        if exists_token and user_info["id"] != exists_token["uid"]:
            self.raise_error(403)
            return

        self.twitter.replace_config(
            "twitter", {
                "access_token": access_token["access_token"],
                "access_token_secret": access_token["access_token_secret"],
                "uid": user_info["id"]
            })

        self.signin(user_info["id"], "twitter")
        self.redirect("/", permanent=False)


class SyncHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        access_token = self.twitter.get_config("twitter")
        self.twitter_oauth.set_access_token(access_token)
        self.twitter.sync_all(self.twitter_oauth)
        self.write("Done!")
