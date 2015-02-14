#!/usr/bin/env python
# -*- coding: utf-8 -*-


from handler.base import BaseHandler
from lib.pager import Pager


class SourceHandler(BaseHandler):

    def get(self, source, page=None):
        if source not in self.source:
            self.raise_error(404)

        _p = int(page) if page else 1
        pagesize = self.config.site["pagesize"]
        posts = self.posts.get_posts(page=_p, pagesize=pagesize, source=source)
        pager = Pager(self.posts.get_posts_count(
            source), pagesize, _p, "/%s/" % source)
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
        p = self.posts.get_history_today(t)
        self.render(
            "past.html", posts_dict=p, yesterday=yesterday, tomorrow=tomorrow, title="past")
