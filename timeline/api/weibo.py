#-*- coding: utf-8 -*-

from .oauth import Oauth
from utils.weibo import APIClient


class WeiboOauth(Oauth):

    def __init__(self, weibo_config, weibo_access=None):
        self._client = APIClient(
            app_key=weibo_config["app_key"], app_secret=weibo_config["app_secret"], redirect_uri=weibo_config["redirect_uri"])
        if weibo_access:
            self._client.set_access_token(
                weibo_access["access_token"], weibo_access["expires_in"])

    def get_authorize_url(self):
        return self._client.get_authorize_url()

    def get_access_token(self, code):
        return self._client.request_access_token(code)

    def set_access_token(self, weibo_access):
        self._client.set_access_token(
            weibo_access["access_token"], weibo_access["expires_in"])

    def get_user_timeline(self):
        return self._client.statuses.user_timeline.get()

    def update_status(self, status):
        self._client.statuses.update.post(status)

    def refresh_token(self):
        return ""
