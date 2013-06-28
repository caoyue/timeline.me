#-*- coding: utf-8 -*-

import web
import json
from config import config
from model.data import ConfigData
from api.weibo import WeiboOauth
from .base import Base


class signin(Base):

    def GET(self):
        client = WeiboOauth(config.OAUTH_DICT["weibo"])
        raise web.seeother(client.get_authorize_url())


class callback(Base):

    def GET(self):
        client = WeiboOauth(config.OAUTH_DICT["weibo"])
        i = web.input()
        r = client.get_access_token(i.code)
        access_token = r.access_token
        expires_in = r.expires_in
        config_value = json.dumps({
            "access_token": access_token,
            "expires_in": expires_in
        })
        ConfigData.set_config_value("weibo_access_token", config_value)
        return "Refresh Token Success!"
