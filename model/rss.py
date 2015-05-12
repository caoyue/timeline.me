#!/usr/bin/env python
# -*- coding: utf-8 -*-


from model.post import Post, PostModel
from lib.timehelper import format_now as now, format_timestr


class RssModel(PostModel):

    def __init__(self, db):
        super(RssModel, self).__init__(db)

    def status_to_post(self, rss, source=None):

        return Post({
            "source": source,
            "category": "rss",
            "origin_id": str(rss.id),
            "url": rss.link,
            "title": rss.title,
            "content": rss.summary,
            "create_time": format_timestr(rss.updated),
            "origin_data": rss
        })

    def sync(self, dict):
        """sync Rss feeds"""

        import feedparser

        print ">> [%s]Rss Sync Start ......" % now()

        try:
            feedparser.RESOLVE_RELATIVE_URIS = 0
            for k, v in dict.items():
                feeds = feedparser.parse(v)
                for entry in feeds.entries:
                    self.save_post(self.status_to_post(entry, k))
        except Exception, e:
            print e
            print ">> Error!"

        print ">> [%s]Rss Sync End." % now()
        print "---------------"
