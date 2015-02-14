#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.web

from handler.base import BaseHandler


class ComposeHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render("compose.html")

    @tornado.web.authenticated
    def post(self):
        status = self.get_argument("status", None)
        message = ""
        checked = {
            "twitter": self.get_argument("twitter", None) == "on",
            "weibo": self.get_argument("weibo", None) == "on",
            "moments": self.get_argument("moments", None) == "on"
        }

        if not status or len(status) > 140:
            return self.render("compose.html", status=status,
                               error=len(status) if status else "0", checked=checked)

        # twitter

        if checked["twitter"]:
            access_token = self.twitter.get_config("twitter")
            if access_token:
                try:
                    self.twitter_oauth.set_access_token(access_token)
                    self.twitter_oauth.update_status(status)
                except Exception, e:
                    message += " * update twitter status failed: %s <br/>" % e
                else:
                    message += " * update twitter status success!<br/>"
            else:
                message += " * <a href='/twitter/signin'>sign in</a> with twitter first!<br/>"

        # weibo

        if checked["weibo"]:
            access_token = self.weibo.get_config("weibo")
            if access_token:
                try:
                    self.weibo_oauth.set_access_token(access_token)
                    self.weibo_oauth.update_status(status)
                except Exception, e:
                    message += " * update weibo status failed: %s <br/>" % e
                else:
                    message += " * update weibo status success!"
            else:
                message += " * <a href='/weibo/signin'>sign in</a> with weibo first!<br/>"

        # timeline.me
        if checked["moments"]:
            try:
                self.posts.save_post(self.posts.status_to_post(status))
            except Exception, e:
                message += " * update timeline.me status failed: %s <br/>" % e
            else:
                message += " * update timeline.me status success!"

        return self.render("compose.html", status=status, message=message, checked=checked)
