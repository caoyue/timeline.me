#-*- coding: utf-8 -*-

import json
from model.data import MySqlData
from model.data import ConfigData
from config import config


class Statistic(object):

    _db = MySqlData()

    @classmethod
    def get_hour_count(cls, year=None):
        """ group by hour """
        if year:
            cursor = cls._db.execute(
                """SELECT count(id),DATE_FORMAT(create_time,'%%H'),source FROM posts WHERE DATE_FORMAT(create_time,'%%Y') = %s GROUP BY source,DATE_FORMAT(create_time,'%%H')""", year)
        else:
            cursor = cls._db.execute(
                """SELECT count(id),DATE_FORMAT(create_time,'%H'),source FROM posts GROUP BY source,DATE_FORMAT(create_time,'%H')""")

        rows = cursor.fetchall()
        cursor and cursor.close()

        r = {}
        for row in rows:
            if row[2] not in r:
                r[row[2]] = {}
            r[row[2]][row[1]] = row[0]

        result = []
        result.append(["Hour"])
        for x in xrange(0, 24):
            result.append(["%dh" % x])
            for s in config.SOURCE:
                if not x:
                    result[0].append(s)
                if s in r:
                    # ['Hour', 'source_count', 'source2_count' ...]
                    result[x + 1].append(int(r[s].get("%02d" % x, 0)))
                else:
                    result[x + 1].append(0)

        return result

    @classmethod
    def get_month_count(cls, year=None):
        """ group by month and year """
        if year:
            cursor = cls._db.execute(
                """SELECT count(id),DATE_FORMAT(create_time,'%%m'),source FROM posts WHERE DATE_FORMAT(create_time,'%%Y') = %s GROUP BY source,DATE_FORMAT(create_time,'%%m')""", year)
        else:
            cursor = cls._db.execute(
                """SELECT count(id),DATE_FORMAT(create_time,'%m'),source FROM posts GROUP BY source,DATE_FORMAT(create_time,'%m')""")
        rows = cursor.fetchall()
        cursor and cursor.close()

        r = {}
        for row in rows:
            if row[2] not in r:
                r[row[2]] = {}
            r[row[2]][row[1]] = row[0]

        month_name = ["Jan", "Feb", "Mar", "Apr", "May",
                      "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        result = []
        result.append(["Month"])
        for x in xrange(1, 13):
            result.append([month_name[x - 1]])
            for s in config.SOURCE:
                if x == 1:
                    result[0].append(s)
                if s in r:
                    # ['Month', 'source_count', 'source2_count' ...]
                    result[x].append(int(r[s].get("%02d" % x, 0)))
                else:
                    result[x].append(0)

        return result

    @classmethod
    def get_source_count(cls, year=None):
        if year:
            cursor = cls._db.execute(
                """SELECT source,count(id) FROM posts WHERE DATE_FORMAT(create_time,'%%Y') = %s GROUP BY source""", year)
        else:
            cursor = cls._db.execute(
                """SELECT source,count(id) FROM posts GROUP BY source""")

        rows = cursor.fetchall()
        cursor and cursor.close()

        if rows:
            result = [[str(r[0]), int(r[1])] for r in rows]
            return [["Source", "Count"]] + list(result)
        return [["Source", "Count"]]


class StatisticData(ConfigData):

    @classmethod
    def get_statistic(cls, type, year=None):
        config_name = "statistic_%s_%s" % (type, year if year else "all")
        value = cls.get_config_value(config_name)

        result = None
        if value:
            result = value
        else:
            data = getattr(Statistic, "get_%s_count" % type)(year)
            result = repr(data)

            from datetime import datetime
            if year and 2009 <= int(year) <= datetime.now().year:
                cls.set_config_value(config_name, json.dumps(data))

        return result

    @classmethod
    def set_statistic(cls, type, year=None):
        config_name = "statistic_%s_%s" % (type, year if year else "all")
        result = getattr(Statistic, "get_%s_count" % type)(year)
        cls.set_config_value(config_name, json.dumps(result))
