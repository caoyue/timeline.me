#!/usr/bin/env python
# -*- coding: utf-8 -*-


from handler.base import BaseHandler


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
