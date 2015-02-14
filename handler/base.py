#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.web

from model.post import PostModel
from model.rss import RssModel
from model.twitter import TwitterModel
from model.weibo import WeiboModel
from model.chart import ChartModel

from oauth.twitter import TwitterOauth
from oauth.weibo import WeiboOauth

import config


class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)
        self.jinja2 = self.settings.get("jinja2")

        self.db = self.application.db
        self.cmd = self.application.cmd

        self.config = config
        self.posts = PostModel(self.db)
        self.rss = RssModel(self.db)
        self.twitter = TwitterModel(self.db)
        self.weibo = WeiboModel(self.db)
        self.chart = ChartModel(self.db)

        self.weibo_oauth = WeiboOauth(api=self.config.oauth["weibo"])
        self.twitter_oauth = TwitterOauth(
            api=self.config.oauth["twitter"])

    @property
    def source(self):
        return self.config.feeds.keys() + self.config.oauth.keys() + ["moments"]

    # override

    def get_current_user(self):
        return self._extract_cookie(self.get_secure_cookie("user"))

    def write_error(self, status_code, **kwargs):
        if status_code == 403:
            self.write("403 Forbidden!")
        elif status_code == 404:
            self.render("404.html")
        else:
            self.write("%s Error!" % status_code)

    def render(self, template_name, **template_vars):
        html = self.render_string(template_name, **template_vars)
        self.write(html)

    def render_string(self, template_name, **template_vars):
        template_vars["site"] = self.config.site
        template_vars["source"] = self.source
        template_vars["links"] = self.config.links

        template_vars["xsrf_form_html"] = self.xsrf_form_html
        template_vars["current_user"] = self.current_user
        template_vars["request"] = self.request
        template_vars["request_handler"] = self
        template = self.jinja2.get_template(template_name)
        return template.render(**template_vars)

    def render_from_string(self, template_string, **template_vars):
        template = self.jinja2.from_string(template_string)
        return template.render(**template_vars)

    # function

    def _extract_cookie(self, cookie):
        if not cookie:
            return None
        user = cookie.split("||")
        if user and len(user) == 2:
            return {"uid": user[0], "signin_type": user[1]}
        return None

    def signin(self, uid, signin_type):
        self.set_secure_cookie("user", "%s||%s" % (uid, signin_type))

    def signout(self):
        self.clear_cookie("user")

    def raise_error(self, status_code):
        raise tornado.web.HTTPError(status_code)
