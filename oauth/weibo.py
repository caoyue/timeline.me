#!/usr/bin/env python
# -*- coding: utf-8 -*-

from oauth.base import Oauth


class WeiboOauth(Oauth):
    NAME = 'weibo'

    def __init__(self, access_token=None):
        super(WeiboOauth, self).__init__(access_token)

    def get_user_timeline(self, count=20, since_id=None, max_id=None):
        params = {
            'count': count,
            'since_id': since_id,
            'max_id': max_id
        }
        return self._client.access_resource(
            'GET',
            url='https://api.weibo.com/2/statuses/user_timeline.json',
            params=dict((k, v) for k, v in params.iteritems() if v)
        )

    def get_user_timeline_by_page(self, count=100, page=1):
        return self._client.access_resource(
            'GET',
            url='https://api.weibo.com/2/statuses/user_timeline.json',
            params={
                'count': count,
                'page': page
            }
        )

    def update_status(self, status):
        self._client.access_resource(
            method='POST',
            url='https://api.weibo.com/2/statuses/update.json',
            data={
                'status': status
            }
        )
