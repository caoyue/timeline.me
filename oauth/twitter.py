#-*- coding: utf-8 -*-

import tweepy


class TwitterOauth(object):

    def __init__(self, api, access=None):
        self._auth = tweepy.OAuthHandler(
            api["consumer_key"],
            api["consumer_secret"],
            api["redirect_uri"]
        )
        self._client = None

        if access:
            self.set_access_token(
                access["access_token"], access["access_token_secret"])
            self._client = tweepy.API(
                self._auth, parser=tweepy.parsers.JSONParser())

    # oauth

    def get_authorize_url(self):
        return self._auth.get_authorization_url()

    def get_request_token(self):
        return self._auth.request_token

    def set_request_token(self, request_token):
        self._auth.request_token = request_token

    def request_access_token(self, oauth_verifier):
        self._auth.get_access_token(oauth_verifier)
        return {
            "access_token": self._auth.access_token,
            "access_token_secret": self._auth.access_token_secret
        }

    def set_access_token(self, access_token):
        self._auth.set_access_token(
            access_token["access_token"], access_token["access_token_secret"])
        self._client = tweepy.API(
            self._auth, parser=tweepy.parsers.JSONParser())

    # api

    def get_user_timeline(self, count=20, since_id=None, max_id=None):
        return self._client.user_timeline(count=count, since_id=since_id, max_id=max_id)

    def update_status(self, status):
        self._client.update_status(status)

    def get_user_info(self):
        return self._client.me()
