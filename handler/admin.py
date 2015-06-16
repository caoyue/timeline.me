#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.web

from handler.base import BaseHandler


class AdminHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render("admin.html", title="admin")


class UserHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.write("signin type: %s <br/> uid: %s" %
                   (self.current_user["signin_type"], self.current_user["uid"]))


class SigninHandler(BaseHandler):

    def get(self):
        accounts = self.binded_accounts
        self.render(
            "signin.html", accounts=accounts if accounts else self.config.oauth, title="sign in")


class SignoutHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.signout()
        self.redirect("/", permanent=False)


class CustomHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        c = self.posts.get_index_source()
        self.render("custom.html", all=self.source,
                    custom=c if c else [], title="custom")

    @tornado.web.authenticated
    def post(self):
        r = self.get_arguments('source')
        self.posts.set_index_source(r)
        return self.render("custom.html", all=self.source, custom=r, title="custom")


class AccountHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        accounts = {
            "weibo": self.weibo.get_access_token(),
            "twitter": self.twitter.get_access_token()
        }
        return self.render(
            "account.html", accounts=accounts, all=self.config.oauth, title="accounts")


class ComposeHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render("compose.html", title="compose")

    @tornado.web.authenticated
    def post(self):
        status = self.get_argument("status", None)
        message = ""
        checked = self.get_arguments('compose')

        if not status or len(status) > 140:
            return self.render("compose.html", status=status,
                               error=len(status) if status else "0", checked=checked)

        # twitter
        if "twitter" in checked:
            access_token = self.twitter.get_access_token()
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

        if "weibo" in checked:
            access_token = self.weibo.get_access_token()
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

        # monments
        if "moments" in checked:
            try:
                self.moments.compose(status)
            except Exception, e:
                message += " * update timeline.me status failed: %s <br/>" % e
            else:
                message += " * update timeline.me status success!"

        return self.render("compose.html", status=status, message=message, checked=checked, title="compose")
