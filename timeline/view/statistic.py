#-*- coding: utf-8 -*-

from .base import Base
from model.statistic import StatisticData
from utils import mytime


class index(Base):

    def GET(self, *year):
        if year:
            year = year[0]

        hour_count = StatisticData.get_statistic("hour", year)
        month_count = StatisticData.get_statistic("month", year)
        source_count = StatisticData.get_statistic("source", year)

        now = mytime.get_time().year
        year_list = reversed(range(now - 3, now + 1))
        s = year if year else "all"
        return self.render.statistic(year_list=year_list, year=s, hour_count=hour_count, month_count=month_count, source_count=source_count, title="graph %s - %s" % (s, self.site["title"]))
