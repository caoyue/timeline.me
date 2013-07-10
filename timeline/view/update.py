#-*- coding: utf-8 -*-

import web
import json
from .base import LoginBase
from api.twitter import TwitterOauth
from api.weibo import WeiboOauth
from model.data import ConfigData


class index(LoginBase):

    def GET(self):
        return self.render.update()

    def POST(self):
        message = ""
        status = web.input().status
        if len(status) > 140:
            return self.render.update(status=status, error=len(status))

        # twitter
        twitter_config = ConfigData.get_config_value(
            "twitter_access_token")
        if twitter_config:
            try:
                twitter_client = TwitterOauth(
                    access_token=json.loads(twitter_config))
                twitter_client.update_status(status)
            except Exception, e:
                message += " - Post twitter status failed: %s <br/>" % e
            else:
                message += " - Post twitter status success!<br/>"
        else:
            message += " - <a href='/twitter/singin'>Login</a> with twitter first!<br/>"

        # weibo
        weibo_config = ConfigData.get_config_value("weibo_access_token")
        if weibo_config:
            try:
                weibo_client = WeiboOauth(
                    weibo_access=json.loads(weibo_config))
                weibo_client.update_status(status)
            except Exception, e:
                message += " - Post weibo status failed: %s <br/>" % e
            else:
                message += " - Post weibo status success!"
        else:
            message += " - <a href='/weibo/singin'>Login</a> with weibo first!<br/>"

        return self.render.update(status=status, message=message)
