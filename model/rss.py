#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import json
import datetime

from model.post import Post, PostModel


class RssModel(PostModel):

    def __init__(self, db):
        super(RssModel, self).__init__(db)

    def get_datetime(self, create_time):
        return datetime.datetime(*create_time[:6])

    def status_to_post(self, rss, source=None):
        return Post({
            "source": source,
            "category": "oauth",
            "origin_id": str(rss.id),
            "url": rss.link,
            "title": rss.title,
            "content": rss.summary,
            "create_time": self.get_datetime(rss.updated_parsed),
            "origin_data": rss
        })

    def sync(self, dict):
        """sync Rss feeds"""

        from lib.timehelper import format_now as now
        import feedparser

        print ">> [%s]Rss Sync Start ......" % now()

        try:
            for k, v in dict.items():
                feeds = feedparser.parse(v)
                for entry in feeds.entries:
                    self.save_post(self.status_to_post(entry, k))
        except Exception, e:
            print e
            print ">> Error!"

        print ">> [%s]Rss Sync End." % now()
        print "---------------"
