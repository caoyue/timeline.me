#-*- coding: utf-8 -*-

from config import config
from rss_sync import rss_sync
from weibo_sync import weibo_sync
from twitter_sync import twitter_sync


def sync_timeline():
    rss_sync(config.FEEDS_DICT)
    weibo_sync(config.OAUTH_DICT["weibo"])
    twitter_sync(config.OAUTH_DICT["twitter"])
