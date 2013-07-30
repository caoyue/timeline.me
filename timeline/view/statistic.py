#-*- coding: utf-8 -*-

from .base import Base
from model.statistic import Statistic
from utils import mytime


class index(Base):

    def GET(self, *year):
        if year:
            year = year[0]
        hour_count = Statistic.get_hour_count(year)
        month_count = Statistic.get_month_count(year)
        source_count = Statistic.get_source_count(year)

        now = mytime.get_time().year
        year_list = reversed(range(now - 3, now + 1))
        s = year if year else "all"
        return self.render.statistic(year_list=year_list, year=s, hour_count=hour_count, month_count=month_count, source_count=source_count, title="graph %s - %s" % (s, self.site["title"]))
