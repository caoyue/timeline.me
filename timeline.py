#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
reload(sys)
sys.setdefaultencoding("utf8")

import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.web

from jinja2 import Environment, FileSystemLoader

import handler.index
import handler.weibo
import handler.twitter

from lib.db import Commander, connect
import config


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
            (r"/signin", handler.twitter.SigninHandler),
            (r"/signout", handler.index.SignoutHandler),
            (r"/weibo/signin", handler.weibo.SigninHandler),
            (r"/weibo/callback", handler.weibo.CallbackHandler),
            (r"/weibo/sync", handler.weibo.SyncHandler),
            (r"/twitter/signin", handler.twitter.SigninHandler),
            (r"/twitter/callback", handler.twitter.CallbackHandler),
            (r"/twitter/sync", handler.twitter.SyncHandler),
            (r"/rss/sync", handler.rss.SyncHandler),
            (r"/test", handler.index.TestHandler)
        ]

        tornado.web.Application.__init__(self, handlers, **settings)

        self.db = connect(config.mysql)
        self.cmd = Commander(self.db)


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
