#-*- coding: utf-8 -*-

import web
import json
from config import config
from model.data import ConfigData
from model.login import Login
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
        config_value = {
            "access_token": access_token,
            "expires_in": expires_in
        }

        try:
            client.set_access_token(config_value)
            user_info = client.get_user_info()
        except Exception, e:
            return "Error! Message: %s" % e

        user_config = ConfigData.get_config_value("weibo_user")
        if user_config and user_info["id"] != user_config["id"]:
            return "User Forbiden!"
        ConfigData.set_config_value(
            "weibo_access_token", json.dumps(config_value))
        Login.login()
        raise web.seeother("/")
