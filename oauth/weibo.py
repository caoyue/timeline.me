#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.weibo import APIClient


class WeiboOauth(object):

    def __init__(self, api, access=None):
        self._client = APIClient(
            app_key=api["app_key"],
            app_secret=api["app_secret"],
            redirect_uri=api["redirect_uri"]
        )
        if access:
            self.set_access_token(access)

    # oauth

    def get_authorize_url(self):
        return self._client.get_authorize_url()

    def request_access_token(self, code):
        return self._client.request_access_token(code)

    def set_access_token(self, access_token):
        self._client.set_access_token(
            access_token["access_token"], access_token["expires_in"])

    # api

    def get_user_uid(self):
        return self._client.account.get_uid.get()

    def get_user_timeline(self, count=20, since_id=None, max_id=None):
        return self._client.statuses.user_timeline.get(count=count, since_id=since_id, max_id=max_id)

    def get_user_timeline_by_page(self, count=100, page=1):
        return self._client.statuses.user_timeline.get(count=count, page=page)

    def update_status(self, status):
        self._client.statuses.update.post(status=status)
