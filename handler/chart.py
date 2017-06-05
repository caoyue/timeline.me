#!/usr/bin/env python
# -*- coding: utf-8 -*-


from handler.base import BaseHandler


class ChartHandler(BaseHandler):

    def get(self, year=None):
        from lib.timehelper import now

        y = now().year
        year_list = list(range(y, y - 4, -1))

        if year:
            i = int(year)
            if i > y or i < 2005:
                self.redirect("/chart", permanent=False)

        hour = self.chart.get_cache(
            type="hour", source_list=self.source, year=year)
        month = self.chart.get_cache(
            type="month", source_list=self.source, year=year)
        sources = self.chart.get_cache(
            type="source", source_list=self.source, year=year)
        self.render("chart.html", hour=hour, month=month, sources=sources, year=year,
                    year_list=year_list, title="chart")
