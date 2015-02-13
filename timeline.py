#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
reload(sys)
sys.setdefaultencoding("utf8")

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
import handler.compose

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
            (r"/timeline/(\d+)", handler.index.IndexHandler),
            (r"/user", handler.index.UserHandler),
            (r"/signin", handler.index.SigninHandler),
            (r"/signout", handler.index.SignoutHandler),
            (r"/weibo/signin", handler.weibo.SigninHandler),
            (r"/weibo/callback", handler.weibo.CallbackHandler),
            (r"/weibo/sync", handler.weibo.SyncHandler),
            (r"/twitter/signin", handler.twitter.SigninHandler),
            (r"/twitter/callback", handler.twitter.CallbackHandler),
            (r"/twitter/sync", handler.twitter.SyncHandler),
            (r"/feed", handler.rss.FeedHandler),
            (r"/rss/sync", handler.rss.SyncHandler),
            (r"/past", handler.post.PastHandler),
            (r"/past/([0-9]{4}-[0-9]{2}-[0-9]{2})", handler.post.PastHandler),
            (r"/s/([^/]+)", handler.post.SourceHandler),
            (r"/s/([^/]+)/(\d+)", handler.post.SourceHandler),
            (r"/ping", handler.index.PingHandler),
            (r"/admin", handler.index.AdminHandler),
            (r"/compose", handler.compose.ComposeHandler),
            (r".*", handler.index.NotFoundHandler)
        ]

        tornado.web.Application.__init__(self, handlers, **settings)

        self.db = connect(config.mysql)
        self.cmd = Commander(self.db)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port if options.port != 80 else 8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
