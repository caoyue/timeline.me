#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import web
import json
from model.data import ConfigData
from model.login import Login
from api.twitter import TwitterOauth
from .base import Base


class signin(Base):

    def GET(self):
        client = TwitterOauth()
        request_token = client.get_request_token()
        url = client.get_authorize_url()
        ConfigData.set_config_value(
            "twitter_request_token", json.dumps(request_token))
        raise web.seeother(url)


class callback(Base):

    def GET(self):
        client = TwitterOauth()
        request_token = ConfigData.get_config_value(
            "twitter_request_token")
        i = web.input()
        client.set_request_token(json.loads(request_token))
        access_token = client.get_access_token(i.oauth_verifier)

        user_info = client.get_user_info()

        user_id = ConfigData.get_config_value("twitter_user_id")
        print user_id, user_info["id"]
        if not user_id:
            ConfigData.set_config_value(
                "twitter_user_id", user_info["id"])
        elif str(user_id) != str(user_info["id"]):
            Login.logout()
            return "User Forbiden!"

        ConfigData.set_config_value(
            "twitter_access_token", json.dumps(access_token))
        Login.login()
        raise web.seeother("/")
