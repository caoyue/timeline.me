#-*- coding: utf-8 -*-

import tweepy
from .oauth import Oauth


class TwitterOauth(Oauth):

    def __init__(self, twitter_config, access_token=None):
        self._auth = tweepy.OAuthHandler(
            twitter_config["consumer_key"], twitter_config["consumer_secret"], twitter_config["redirect_uri"])
        if access_token:
            self._auth.set_access_token(
                access_token["access_token"], access_token["access_token_secret"])
            self._client = tweepy.API(
                self._auth, parser=tweepy.parsers.JSONParser())

    def get_user_info(self):
        self._client = tweepy.API(
            self._auth, parser=tweepy.parsers.JSONParser())
        return self._client.me()

    def get_authorize_url(self):
        return self._auth.get_authorization_url()

    def get_request_token(self):
        return {"request_token": self._auth.request_token.key,
                "request_token_secret": self._auth.request_token.secret}

    def set_request_token(self, request_token):
        self._auth.set_request_token(
            request_token["request_token"], request_token["request_token_secret"])

    def get_access_token(self, oauth_verifier):
        self._auth.get_access_token(oauth_verifier)
        return {"access_token": self._auth.access_token.key,
                "access_token_secret": self._auth.access_token.secret}

    def set_access_token(self, access_token):
        self._auth.set_access_token(
            access_token["access_token"], access_token["access_token_secret"])
        self._client = tweepy.API(
            self._auth, parser=tweepy.parsers.JSONParser())

    def get_user_timeline(self, count=20, since_id=None, max_id=None):
        return self._client.user_timeline(count=count, since_id=since_id, max_id=max_id)

    def update_status(self, status):
        self._client.update_status(status)

    def refresh_token(self):
        pass
