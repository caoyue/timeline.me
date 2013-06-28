#-*- coding: utf-8 -*-

import web
import json
from config import config
from model.data import ConfigData
from api.twitter import TwitterOauth
from .base import Base


class signin(Base):

    def GET(self):
        client = TwitterOauth(config.OAUTH_DICT["twitter"])
        url = client.get_authorize_url()
        ConfigData.set_config_value(
            "twitter_request_token", json.dumps(client.get_request_token()))
        raise web.seeother(url)


class callback(Base):

    def GET(self):
        client = TwitterOauth(config.OAUTH_DICT["twitter"])
        request_token = ConfigData.get_config_value(
            "twitter_request_token")
        i = web.input()
        client.set_request_token(json.loads(request_token))
        access_token = client.get_access_token(i.oauth_verifier)
        ConfigData.set_config_value(
            "twitter_access_token", json.dumps(access_token))
        return "Refresh Token Success!"
