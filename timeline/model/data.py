#-*- coding: utf-8 -*-

import MySQLdb
from post import Post
from config import config


class MySqlData(object):

    def __init__(self):
        try:
            self._conn = MySQLdb.connect(
                host=config.DB_HOST,
                port=config.DB_PORT,
                user=config.DB_USR,
                passwd=config.DB_PSW,
                db=config.DB_NAME,
                use_unicode=True,
                charset="utf8")
        except Exception, e:
            print "connect db fail : %s" % e
            self._conn = None

    def execute(self, *sql, **param):
        cursor = None
        try:
            cursor = cursor or self._conn.cursor()
            cursor.execute(*sql, **param)
        except Exception, e:
            print "excute fail : %s" % e
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
        cursor = None
        count = None
        try:
            if source:
                cursor = cls._db.execute(
                    """select count(id) from posts where source = %s""", source)
                count = cursor.fetchone()
            else:
                cursor = cls._db.execute("""select count(id) from posts""")
                count = cursor.fetchone()
        except Exception, e:
            print "execute fail : %s" % e
        finally:
            cursor.close() if cursor else cursor
        return int(count[0]) if count else 0

    @classmethod
    def get_posts(cls, page=1, pagesize=10):
        cursor = None
        rows = None
        try:
            cursor = cls._db.execute(
                """select * from posts order by create_time desc limit %s,%s""", ((page - 1) * pagesize, pagesize))
            rows = cursor.fetchall()
        except Exception, e:
            print "execute fail : %s" % e
        finally:
            cursor.close() if cursor else cursor
        if rows:
            return [cls.data_to_post(row) for row in rows]
        return []

    @classmethod
    def get_source_posts(cls, source, page=1, pagesize=10):
        cursor = None
        rows = None
        try:
            cursor = cls._db.execute("""select * from posts where source = %s order by create_time desc limit %s,%s""", (
                source, (page - 1) * pagesize, pagesize))
            rows = cursor.fetchall()
        except Exception, e:
            print "excute fail : %s" % e
        finally:
            cursor.close() if cursor else cursor
        if rows:
            return [cls.data_to_post(row) for row in rows]
        return []

    @classmethod
    def get_last_post(cls, source):
        cursor = None
        try:
            cursor = cls._db.execute(
                """select * from posts where source = %s order by create_time desc limit 0,1""", source)
            row = cursor.fetchone()
        except Exception, e:
            print "execute fail : %s" % e
        finally:
            cursor.close() if cursor else cursor
        if row:
            return cls.data_to_post(row)
        return None

    @classmethod
    def is_in_database(cls, post):
        cursor = None
        row = None
        try:
            cursor = cls._db.execute(
                """select * from posts where title = %s and create_time = %s""", (post.title, post.create_time))
            row = cursor.fetchall()
        except Exception, e:
            print "excute fail : %s" % e
        finally:
            cursor.close() if cursor else cursor
        return row

    @classmethod
    def save_post(cls, post):
        cursor = None
        if not cls.is_in_database(post):
            try:
                cursor = cls._db.execute(
                    """insert into posts (source, category, orgin_id, url, title, content, create_time, orgin_data) values (%s,%s,%s,%s,%s,%s,%s,%s)""", (post.source, post.category, post.orgin_id, post.url, post.title, post.content, post.create_time, post.orgin_data))
                cls._db.commit()
            except Exception, e:
                print "log : %s" % e
                cls._db.rollback()
            finally:
                cursor.close() if cursor else cursor


class ConfigData(object):

    _db = MySqlData()

    @classmethod
    def get_config_value(cls, config_name):
        cursor = None
        row = None
        try:
            cursor = cls._db.execute(
                """select * from configs where config_name = %s""", config_name)
            row = cursor.fetchone()
        except Exception, e:
            print "execute fail : %s" % e
        finally:
            cursor.close() if cursor else cursor
        if row:
            return row[2]
        return None

    @classmethod
    def set_config_value(cls, config_name, config_value):
        cursor = None
        try:
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
        except Exception, e:
            print "execute fail : %s" % e
            cls._db.rollback()
        finally:
            cursor.close() if cursor else cursor
