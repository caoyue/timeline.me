#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.db import connect, Commander
from model.rss import RssModel
from model.twitter import TwitterModel
from model.weibo import WeiboModel
from oauth.twitter import TwitterOauth
from oauth.weibo import WeiboOauth
import config


db = connect(config.mysql)


class Twitter(object):

    @classmethod
    def sync(self):
        twitter = TwitterModel(db)
        access_token = twitter.get_access_token()
        twitter_oauth = TwitterOauth(access_token)
        twitter.sync(twitter_oauth)


class Weibo(object):

    @classmethod
    def sync(self):
        weibo = WeiboModel(db)
        access_token = weibo.get_access_token()
        weibo_oauth = WeiboOauth(access_token)
        weibo.sync(weibo_oauth)


class Rss(object):

    @classmethod
    def sync(self):
        rss = RssModel(db)
        rss.sync(config.feeds)

if __name__ == '__main__':
    Twitter.sync()
    Weibo.sync()
    Rss.sync()
