#-*- coding: utf-8 -*-

from model.data import PastData
from utils import mytime
from .base import Base


class index(Base):

    def GET(self, *now):
        t = None
        if now:
            t = mytime.get_time_from_string(time_str=now[0])
        else:
            t = mytime.get_time()
        p = PastData.get_history_today(t)
        return self.render.past(posts_dict=p, title="past")
