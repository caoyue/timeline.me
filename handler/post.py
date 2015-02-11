#!/usr/bin/env python
# -*- coding: utf-8 -*-


from handler.base import BaseHandler
from lib.pager import Pager


class SourceHandler(BaseHandler):

    def get(self, source, page=None):
        if source not in self.source:
            self.raise_error(404)

        _p = int(page) if page else 1
        posts = self.post.get_posts(page=_p, pagesize=10, source=source)
        pager = Pager(self.post.get_posts_count(
            source), 10, _p, "/s/%s/" % source)
        self.render("index.html", posts=posts, pager=pager, title=source)


class PastHandler(BaseHandler):

    def get(self, t=None):
        import lib.timehelper as th

        if t:
            try:
                t = th.parse_timestr(timestr=t)
            except Exception, e:
                self.write("Not a valid date!")
                return
        else:
            t = th.now()
        yesterday = th.format_day_ago(timeobj=t, days=-1)
        tomorrow = th.format_day_ago(timeobj=t, days=1)
        p = self.post.get_history_today(t)
        self.render(
            "past.html", posts_dict=p, yesterday=yesterday, tomorrow=tomorrow, title="past")
