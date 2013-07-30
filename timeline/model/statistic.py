#-*- coding: utf-8 -*-

from model.data import MySqlData
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
        result.append(['Hour'])
        for x in xrange(0, 24):
            result.append([str(x)])
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

        result = []
        result.append(['Month'])
        for x in xrange(1, 13):
            result.append([str(x)])
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

        return rows
