#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pymysql.cursors


def connect(config):
    return pymysql.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        db=config["database"],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


class Commander(object):

    def __init__(self, connection=None):
        if connection:
            self.connection = connection

    def _excute(self, sql, params):
        if type(params) is list:
            params = tuple(params)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, *params)
            self.connection.commit()
        except Exception, e:
            print e

    # CRUD

    def _concat_dict(self, params):
        return ",".join(["%s=%%s" % k for k in params.keys()])

    def _query_sql(self, table, fields=["*"], where=None, orderby=None,
                   desc=True, page=None, pagesize=None):
        limit = "LIMIT %s,%s" % (
            (page - 1) * pagesize, pagesize) if page and pagesize else ""
        sql = """SELECT %s FROM %s %s %s %s %s""" % (
            ",".join(fields),
            table,
            "WHERE %s" % where if where else "",
            "ORDER BY %s" % orderby if orderby else "",
            "DESC" if desc and orderby else "",
            limit
        )
        return sql

    def excute_sql(self, sql):
        result = []
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
        except Exception, e:
            print e
        return result

    def query(self, table, fields=["*"], where=None, orderby=None,
              desc=True, page=None, pagesize=None):
        sql = self._query_sql(
            table, fields, where, orderby, desc, page, pagesize)
        print sql
        return self.excute_sql(sql)

    def get(self, table, fields=["*"], where=None, orderby=None, desc=True):
        """Returns the singular row."""

        rows = self.query(table, fields, where, orderby, desc, 1, 1)
        return rows[0] if rows else None

    def count(self, table, where=None):
        return self.get(table, ["count(*)"], where)["count(*)"]

    def save(self, table, values):
        sql = """INSERT INTO %s (%s) VALUES (%s)""" % (
            table,
            ", ".join(values.keys()),
            ", ".join(["%s"] * len(values.keys()))
        )
        params = values.values()
        self._excute(sql, params)

    def replace(self, table, values):
        sql = """REPLACE INTO %s (%s) VALUES (%s)""" % (
            table,
            ", ".join(values.keys()),
            ", ".join(["%s"] * len(values.keys()))
        )
        params = values.values()
        print "params:"
        print params
        self._excute(sql, params)

    def update(self, table, values, where=None):
        sql = """UPDATE %s SET %s %s """ % (
            table, self._concat_dict(values), "WHERE %s" % where if where else "")
        params = values.values()
        self._excute(sql, params)

    def delete(self, table, where):
        sql = """DELETE FROM %s WHERE %s"""
        params = (table, where)
        self._excute(sql, params)
