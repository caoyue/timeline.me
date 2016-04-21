#!/usr/bin/env python
# -*- coding: utf-8 -*-

from oauth2py.client import OauthClient


class Oauth(object):
    NAME = ''

    def __init__(self, access_token=None):
        self._client = OauthClient.load(self.NAME)
        if access_token:
            self._client.set_access_token(access_token)

    def get_authorize_url(self):
        return self._client.get_login_url()

    def get_user_info(self, query):
        return self._client.get_user_info(query)

    def request_access_token(self):
        return self._client.get_access_token()

    def set_access_token(self, access_token):
        self._client.set_access_token(access_token)
