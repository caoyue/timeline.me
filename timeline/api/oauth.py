#-*- coding: utf-8 -*-

import urllib
import requests


class Oauth(object):

    authorize_uri = ''
    access_token_uri = ''

    def __init__(
            self, app_key=None, app_secret=None, redirect_uri=None, access_token=None, refresh_token=None):
        self.apikey = app_key
        self.apikey_secret = app_secret
        self.redirect_uri = redirect_uri
        self.access_token = access_token
        self.refresh_token = refresh_token

    def get_authorize_url(self):
        p = {
            'client_id': self.app_key,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
        }

        p = urllib.urlencode(p)
        uri = '%s?%s' % (self.authorize_uri, p)
        return uri

    def get_request_token(self):
        pass

    def set_request_token(self, request_token):
        pass

    def get_access_token(self, code):
        data = {
            "client_id": self.app_key,
            "client_secret": self.app_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
            "code": code
        }
        app_access_token = requests.post(self.access_token_url, data=data)
        result = app_access_token.json()
        if "access_token" in result:
            return result["access_token"]
        print "get access token failed!"
        return None

    def set_access_token(self, access_token):
        self.access_token = access_token

    def refresh_token(self, refresh_token):
        self.refresh_token = refresh_token

    def get_user_timeline(self, count=20, since_id=None, max_id=None):
        pass

    def update_status(self, status):
        pass

    def get_user_info():
        pass
