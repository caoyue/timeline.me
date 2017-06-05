#!/usr/bin/env python
# -*- coding: utf-8 -*-


from model.base import BaseModel


class ChartModel(BaseModel):

    def __init__(self, db):
        super(ChartModel, self).__init__(db)

    def get_hour_count(self, source_list, year=None):
        """ group by hour """

        sql = ""
        if year:
            sql = """SELECT count(id) as count,DATE_FORMAT(create_time,'%H') as hour,source FROM posts WHERE DATE_FORMAT(create_time,'%Y') = """ + \
                year + """ GROUP BY source,DATE_FORMAT(create_time,'%H')"""
        else:
            sql = """SELECT count(id) as count,DATE_FORMAT(create_time,'%H') as hour,source FROM posts GROUP BY source,DATE_FORMAT(create_time,'%H')"""

        rows = self.excute_sql(sql)

        d = {}
        for s in source_list:
            d[s] = ["0" for x in range(0, 24)]

        for r in rows:
            d[r["source"]][int(r["hour"])] = str(r["count"])
        return d

    def get_month_count(self, source_list, year=None):
        """ group by month and year """

        sql = ""
        if year:
            sql = """SELECT count(id) as count, DATE_FORMAT(create_time,'%m') as month, source FROM posts WHERE DATE_FORMAT(create_time,'%Y') = """ + \
                year + """ GROUP BY source,DATE_FORMAT(create_time,'%m')"""
        else:
            sql = """SELECT count(id) as count, DATE_FORMAT(create_time,'%m') as month, source FROM posts GROUP BY source,DATE_FORMAT(create_time,'%m')"""

        rows = self.excute_sql(sql)

        d = {}
        for s in source_list:
            d[s] = ["0" for x in range(0, 12)]

        for r in rows:
            d[r["source"]][int(r["month"]) - 1] = str(r["count"])
        return d

    def get_source_count(self, source_list, year=None):

        sql = ""
        if year:
            sql = """SELECT source,count(id) as count FROM posts WHERE DATE_FORMAT(create_time,'%Y') = """ + \
                year + """ GROUP BY source"""
        else:
            sql = """SELECT source,count(id) as count FROM posts GROUP BY source"""

        return self.excute_sql(sql)

    def get_count(self, type, source_list, year=None):
        return getattr(self, "get_%s_count" % type)(source_list, year)

    def get_cache(self, type, source_list, year=None):
        import json
        from lib.timehelper import now, datediff

        name = "chart_cache_%s_%s" % (type, year if year else "all")
        value = self.get_config_time(name)
        tnow = now().replace(tzinfo=None)

        if value and (year and year != str(tnow.year) or abs(datediff(value["create_time"], tnow)) <= 1):
            return value["value"]
        else:
            data = self.get_count(type, source_list, year)
            self.replace_config(name, data)
            return data
