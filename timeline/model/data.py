#-*- coding: utf-8 -*-

import datetime
import MySQLdb
from post import Post
from config import config
from utils.logger import logging

log = logging.getLogger(__file__)


def connect_mysql():
    try:
        conn = MySQLdb.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            user=config.DB_USR,
            passwd=config.DB_PSW,
            db=config.DB_NAME,
            use_unicode=True,
            charset="utf8")
        return conn
    except Exception, e:
        log.warning("connect db fail : %s" % e)
        return None


class MySqlData(object):

    def __init__(self):
        self._conn = connect_mysql()

    def _reconnect(self):
        self._conn = connect_mysql()
        return self._conn

    def execute(self, *sql, **param):
        cursor = None
        try:
            cursor = self._conn.cursor()
            cursor.execute(*sql, **param)
        except MySQLdb.Error, e:
            log.warning("excute [%s] fail : %s" % (sql, e))
            self._conn and self._conn.close()
            self._reconnect()

            cursor = self._conn.cursor()
            cursor.execute(*sql, **param)
        return cursor

    def commit(self):
        return self._conn and self._conn.commit()

    def rollback(self):
        return self._conn and self._conn.rollback()


class PostData(object):

    _db = MySqlData()

    @classmethod
    def data_to_post(cls, data):
        return Post(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])

    @classmethod
    def get_posts_count(cls, source=None):
        if source:
            cursor = cls._db.execute(
                """SELECT count(id) FROM posts WHERE source = %s""", source)
            count = cursor.fetchone()
        else:
            cursor = cls._db.execute("""SELECT count(id) FROM posts""")
            count = cursor.fetchone()

        cursor and cursor.close()

        return int(count[0]) if count else 0

    @classmethod
    def get_posts(cls, page=1, pagesize=10, orderby='create_time'):
        cursor = cls._db.execute(
            """SELECT * FROM posts ORDER BY %s DESC LIMIT %%s,%%s""" % orderby, ((page - 1) * pagesize, pagesize))
        rows = cursor.fetchall()

        cursor and cursor.close()
        if rows:
            return [cls.data_to_post(row) for row in rows]
        return []

    @classmethod
    def get_posts_since(cls, since_id):
        cursor = cls._db.execute(
            """SELECT * FROM posts WHERE id > %s""", since_id)
        rows = cursor.fetchall()

        cursor and cursor.close()

        if rows:
            return [cls.data_to_post(row) for row in rows]
        return []

    @classmethod
    def get_source_posts(cls, source, page=1, pagesize=10):
        cursor = cls._db.execute("""SELECT * FROM posts WHERE source = %s ORDER BY create_time DESC LIMIT %s,%s""", (
            source, (page - 1) * pagesize, pagesize))
        rows = cursor.fetchall()

        cursor and cursor.close()

        if rows:
            return [cls.data_to_post(row) for row in rows]
        return []

    @classmethod
    def get_last_post(cls, source):
        cursor = cls._db.execute(
            """SELECT * FROM posts WHERE source = %s ORDER BY create_time DESC LIMIT 0,1""", source)
        row = cursor.fetchone()

        cursor and cursor.close()

        if row:
            return cls.data_to_post(row)
        return None

    @classmethod
    def is_in_database(cls, post):
        cursor = cls._db.execute(
            """SELECT id FROM posts WHERE url = %s""", post.url)
        row = cursor.fetchall()

        cursor and cursor.close()

        return row

    @classmethod
    def save_post(cls, post):
        if not cls.is_in_database(post):
            cursor = cls._db.execute(
                """INSERT INTO posts (source, category, origin_id, url, title, content, create_time, origin_data) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""", (post.source, post.category, post.origin_id, post.url, post.title, post.content, post.create_time, post.origin_data))
            cls._db.commit()

            cursor and cursor.close()
            return True
        return False


class ConfigData(object):

    _db = MySqlData()

    @classmethod
    def get_config_value(cls, config_name):
        cursor = cls._db.execute(
            """SELECT * FROM configs WHERE config_name = %s""", config_name)
        row = cursor.fetchone()

        cursor and cursor.close()

        if row:
            return row[2]
        return None

    @classmethod
    def set_config_value(cls, config_name, config_value):
        cursor = cls._db.execute(
            """SELECT * FROM configs WHERE config_name = %s""", config_name)
        row = cursor.fetchall()

        if row:
            cursor = cls._db.execute(
                """UPDATE configs SET config_value = %s WHERE config_name = %s""", (config_value, config_name))
        else:
            cursor = cls._db.execute(
                """INSERT INTO configs (config_name, config_value) VALUES (%s,%s)""", (config_name, config_value))
            cls._db.commit()

        cursor and cursor.close()


class PastData(PostData):

    _db = MySqlData()

    @classmethod
    def get_id_by_date(cls, start, end):
        cursor = cls._db.execute(
            """SELECT * FROM posts WHERE create_time >= %s AND create_time <= %s ORDER BY create_time DESC""", (start, end))
        rows = cursor.fetchall()

        cursor and cursor.close()

        if rows:
            return [cls.data_to_post(row) for row in rows]
        return []

    @classmethod
    def get_history_today(cls, now):
        def get_time_string(time):
            return time.strftime("%Y-%m-%d")
        years = range(now.year - 1, 2005, -1)
        dates = [("%s-%s" % (y, now.strftime("%m-%d")),
                  "%s-%s" % (y, (now + datetime.timedelta(days=1)).strftime("%m-%d"))) for y in years]
        posts_list = [cls.get_id_by_date(d[0], d[1]) for d in dates]

        p = {}
        for posts in posts_list:
            if posts:
                p[get_time_string(posts[0].create_time)] = posts
        return p
