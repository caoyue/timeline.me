#!/usr/bin/env python
# -*- coding: utf-8 -*-


import torndb


def connect(config):
    return torndb.Connection(
        host=config["host"],
        database=config["database"],
        user=config["user"],
        password=config["password"],
        charset='utf8mb4'
    )


class Commander(object):

    def __init__(self, db=None):
        if db:
            self.db = db

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
            "ORDER BY '%s'" % orderby if orderby else "",
            "DESC" if desc and orderby else "",
            limit
        )
        return sql

    def query(self, table, fields=["*"], where=None, orderby=None,
              desc=True, page=None, pagesize=None):
        return self.db.query(self._query_sql(table, fields, where, orderby, desc, page, pagesize))

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
        return self.db.execute(sql, *params)

    def replace(self, table, values):
        sql = """REPLACE INTO %s (%s) VALUES (%s)""" % (
            table,
            ", ".join(values.keys()),
            ", ".join(["%s"] * len(values.keys()))
        )
        params = values.values()
        return self.db.execute(sql, *params)

    def update(self, table, values, where=None):
        sql = """UPDATE %s SET %s %s """ % (
            table, self._concat_dict(values), "WHERE %s" % where if where else "")
        params = values.values()
        return self.db.execute(sql, *params)

    def delete(self, table, where):
        sql = """DELETE FROM %s WHERE %s""" % (table, where)
        return self.db.execute(sql)
