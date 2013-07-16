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
            cursor = cursor or self._conn.cursor()
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
                """select count(id) from posts where source = %s""", source)
            count = cursor.fetchone()
        else:
            cursor = cls._db.execute("""select count(id) from posts""")
            count = cursor.fetchone()

        if cursor:
            cursor.close()

        return int(count[0]) if count else 0

    @classmethod
    def get_posts(cls, page=1, pagesize=10):
        cursor = cls._db.execute(
            """select * from posts order by create_time desc limit %s,%s""", ((page - 1) * pagesize, pagesize))
        rows = cursor.fetchall()

        if cursor:
            cursor.close()

        if rows:
            return [cls.data_to_post(row) for row in rows]
        return []

    @classmethod
    def get_source_posts(cls, source, page=1, pagesize=10):
        cursor = cls._db.execute("""select * from posts where source = %s order by create_time desc limit %s,%s""", (
            source, (page - 1) * pagesize, pagesize))
        rows = cursor.fetchall()

        if cursor:
            cursor.close()

        if rows:
            return [cls.data_to_post(row) for row in rows]
        return []

    @classmethod
    def get_last_post(cls, source):
        cursor = cls._db.execute(
            """select * from posts where source = %s order by orgin_id desc limit 0,1""", source)
        row = cursor.fetchone()

        if cursor:
            cursor.close()

        if row:
            return cls.data_to_post(row)
        return None

    @classmethod
    def is_in_database(cls, post):
        cursor = cls._db.execute(
            """select id from posts where url = %s""", post.url)
        row = cursor.fetchall()

        if cursor:
            cursor.close()

        return row

    @classmethod
    def save_post(cls, post):
        if not cls.is_in_database(post):
            cursor = cls._db.execute(
                """insert into posts (source, category, orgin_id, url, title, content, create_time, orgin_data) values (%s,%s,%s,%s,%s,%s,%s,%s)""", (post.source, post.category, post.orgin_id, post.url, post.title, post.content, post.create_time, post.orgin_data))
            cls._db.commit()

            if cursor:
                cursor.close()
            return True
        return False


class ConfigData(object):

    _db = MySqlData()

    @classmethod
    def get_config_value(cls, config_name):
        cursor = cls._db.execute(
            """select * from configs where config_name = %s""", config_name)
        row = cursor.fetchone()

        if cursor:
            cursor.close()

        if row:
            return row[2]
        return None

    @classmethod
    def set_config_value(cls, config_name, config_value):
        cursor = cls._db.execute(
            """select * from configs where config_name = %s""", config_name)
        row = cursor.fetchall()

        if row:
            cursor = cls._db.execute(
                """update configs set config_value = %s where config_name = %s""", (config_value, config_name))
        else:
            cursor = cls._db.execute(
                """insert into configs (config_name, config_value) values (%s,%s)""", (config_name, config_value))
            cls._db.commit()

        if cursor:
            cursor.close()


class PastData(PostData):

    _db = MySqlData()

    @classmethod
    def get_id_by_date(cls, start, end):
        cursor = cls._db.execute(
            """select * from posts where create_time >= %s and create_time <= %s order by create_time desc""", (start, end))
        rows = cursor.fetchall()

        if cursor:
            cursor.close()

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

        p = dict()
        for posts in posts_list:
            if posts:
                p[get_time_string(posts[0].create_time)] = posts
        return p
