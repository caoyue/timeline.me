#-*- coding: utf-8 -*-

import web
from model.data import PastData
from utils import mytime
from .base import Base


class index(Base):

    def GET(self, *now):
        t = None
        if now:
            try:
                t = mytime.get_time_from_string(time_str=now[0])
            except Exception:
                raise web.seeother(
                    '/past/%s' % mytime.get_time_now('%Y-%m-%d'))
        else:
            t = mytime.get_time()
        p = PastData.get_history_today(t)
        yesterday = mytime.get_yesterday(t)
        tomorrow = mytime.get_tomorrow(t)
        return self.render.past(posts_dict=p, yesterday=yesterday, tomorrow=tomorrow, title="past")
