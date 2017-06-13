#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

from jinja2 import Environment, FileSystemLoader

import handler.index
import handler.post
import handler.rss
import handler.weibo
import handler.twitter
import handler.admin
import handler.chart

from lib.db import Commander, connect
import config

define("port", default=80, help="port", type=int)


class Application(tornado.web.Application):

    def __init__(self):
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret=config.secret,
            autoescape=None,
            jinja2=Environment(loader=FileSystemLoader(
                os.path.join(os.path.dirname(__file__), "templates")), trim_blocks=True),
            login_url="/signin"
        )

        handlers = [
            (r"/", handler.index.IndexHandler),
            (r"/weibo/signin", handler.weibo.SigninHandler),
            (r"/weibo/bind", handler.weibo.BindHandler),
            (r"/weibo/callback", handler.weibo.CallbackHandler),
            (r"/weibo/sync", handler.weibo.SyncHandler),
            (r"/twitter/signin", handler.twitter.SigninHandler),
            (r"/twitter/bind", handler.twitter.BindHandler),
            (r"/twitter/callback", handler.twitter.CallbackHandler),
            (r"/twitter/sync", handler.twitter.SyncHandler),
            (r"/feed", handler.rss.FeedHandler),
            (r"/rss/sync", handler.rss.SyncHandler),
            (r"/past", handler.post.PastHandler),
            (r"/past/([0-9]{4}-[0-9]{2}-[0-9]{2})", handler.post.PastHandler),
            (r"/chart", handler.chart.ChartHandler),
            (r"/chart/([1,2][0-9]{3})", handler.chart.ChartHandler),
            (r"/ping", handler.index.PingHandler),
            (r"/post/delete/([1-9]\d+)", handler.admin.DeleteHandler),
            (r"/admin", handler.admin.AdminHandler),
            (r"/signin", handler.admin.SigninHandler),
            (r"/signout", handler.admin.SignoutHandler),
            (r"/admin/user", handler.admin.UserHandler),
            (r"/admin/compose", handler.admin.ComposeHandler),
            (r"/admin/custom", handler.admin.CustomHandler),
            (r"/admin/account", handler.admin.AccountHandler),
            (r"/([^/]+)", handler.index.IndexHandler),
            (r"/([^/]+)/(\d+)", handler.index.IndexHandler),
            (r".*", handler.index.NotFoundHandler)
        ]

        tornado.web.Application.__init__(self, handlers, **settings)

        self.db = connect(config.mysql)
        self.cmd = Commander(self.db)
        self.data = {}


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
