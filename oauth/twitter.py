#!/usr/bin/env python
# -*- coding: utf-8 -*-

from oauth.base import Oauth


class TwitterOauth(Oauth):
    NAME = 'twitter'

    def __init__(self, access_token=None):
        super(TwitterOauth, self).__init__(access_token)

    def get_request_token(self):
        return self._client.get_request_token()

    def get_user_info(self, query, request_token):
        return self._client.get_user_info(query, request_token)

    def get_user_timeline(self, count=20, since_id=None, max_id=None):
        params = {
            'count': count,
            'since_id': since_id,
            'max_id': max_id
        }
        return self._client.access_resource(
            'GET',
            url='https://api.twitter.com/1.1/statuses/user_timeline.json',
            params=dict((k, v) for k, v in params.iteritems() if v)
        )

    def update_status(self, status):
        self._client.access_resource(
            'POST',
            url='https://api.twitter.com/1.1/statuses/update.json',
            data={
                'status': status
            }
        )
