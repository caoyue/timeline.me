#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.web
from oauth.weibo import WeiboOauth
from model.weibo import WeiboModel
from oauth.twitter import TwitterOauth
from model.twitter import TwitterModel
from model.rss import RssModel

from config import oauth_dict


class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)
        self.db = self.application.db
        self.cmd = self.application.cmd
        self.weibo_oauth = WeiboOauth(api=oauth_dict["weibo"])
        self.weibo_model = WeiboModel(self.db)
        self.twitter_oauth = TwitterOauth(api=oauth_dict["twitter"])
        self.twitter_model = TwitterModel(self.db)
        self.rss_model = RssModel(self.db)

    # override

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def write_error(self, status_code, **kwargs):
        if status_code == 403:
            self.write("403 Forbidden!")
        else:
            self.write("%s Error!" % status_code)

    # function
    def signin(self, user_id, login_type):
        self.set_secure_cookie("user", "%s||%s" % (user_id, login_type))

    def signout(self):
        self.clear_cookie("user")

    def raise_error(self, status_code):
        raise tornado.web.HTTPError(status_code)
