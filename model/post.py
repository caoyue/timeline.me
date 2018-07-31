#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re

from model.base import BaseModel


class Post(object):

    def __init__(self, dict):
        self.__dict__.update(dict)

    def __repr__(self):
        return repr(self.__dict__)

    __str__ = __repr__

    def _pure_title(self):
        if self.title:
            content = self.title
            pattern = re.compile(
                """[a-zA-Z]+:\/\/[a-zA-Z0-9.]+\.[a-zA-Z0-9.\/]+""")
            matchs = pattern.findall(content)
            if matchs:
                for m in matchs:
                    content = content.replace(
                        m, "")
            return content.strip()
        return self.title

    def _edit_distance(self, str1, str2):
        m, n = len(str1), len(str2)
        ans = [[0 for i in range(n + 1)] for j in range(m + 1)]
        for i in range(m + 1):
            ans[i][n] = m - i
        for i in range(n + 1):
            ans[m][i] = n - i
        m -= 1
        n -= 1
        while m >= 0:
            t = n
            while t >= 0:
                if str1[m] == str2[t]:
                    ans[m][t] = ans[m + 1][t + 1]
                else:
                    ans[m][t] = min(ans[m][t + 1], ans[m + 1]
                                    [t], ans[m + 1][t + 1]) + 1
                t -= 1
            m -= 1
        return ans[0][0]

    def is_duplicate(self, compare):
        if self.category == "oauth" \
                and compare.category == "oauth" \
                and abs(self.create_time.day - compare.create_time.day) == 0 \
                and self._edit_distance(self.title, compare.title) <= 5:
            return True
        return False

    @property
    def dict(self):
        return self.__dict__


class PostModel(BaseModel):

    def __init__(self, db):
        super(PostModel, self).__init__(db)

    # function

    def _row_to_post(self, row):
        return Post(row) if row else None

    def _rows_to_posts(self, rows):
        return [self._row_to_post(row) for row in rows] if rows else []

    def pure_title(self, title):
        """remove links from title"""

        if title:
            pattern = re.compile(
                """[a-zA-Z]+:\/\/[a-zA-Z0-9.]+\.[a-zA-Z0-9.\/]+""")
            matchs = pattern.findall(title)
            if matchs:
                for m in matchs:
                    title = title.replace(m, "")
            return title.strip()
        return title

    def replace_url(self, content):
        """replace link text to html"""

        pattern = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')
        matchs = pattern.findall(content)
        if matchs:
            for m in matchs:
                content = content.replace(
                    m, """<a href="%s" target="_blank">%s</a>""" % (m, m))
        return content

    def is_duplicate(self, post, compare):
        """
        publish in 24 hours and have same tilte
        """

        if abs(post.create_time.day - compare.create_time.day) == 0 \
                and self.pure_title(post) == self.pure_title(compare):
            return True
        return False

    def status_to_post(self, status):
        return status

    # db

    def get_visible_source(self):
        return self.get_config("signin_visible_source")

    def set_visible_source(self, values):
        return self.replace_config("signin_visible_source", values)

    def get_posts_count(self, source=None):
        w = None
        if source:
            w = "source in ('%s')" % "','".join(source)
        return self.count(
            "posts",
            where=w
        )

    def get_posts(self, page=1, pagesize=10, source=None, orderby='create_time'):
        w = None
        if source:
            w = "source in ('%s')" % "','".join(source)
        rows = self.query(
            table="posts",
            where=w,
            orderby=orderby,
            page=page,
            pagesize=pagesize
        )
        return self._rows_to_posts(rows)

    def get_posts_since(self, since_id):
        rows = self.query(
            table="posts",
            orderby="create_time",
            where="id > %s" % since_id if since_id else None
        )
        return self._rows_to_posts(rows)

    def get_last_post(self, source=None):
        row = self.get(
            table="posts",
            orderby="create_time",
            where="source = '%s'" % source if source else None,
        )
        return self._row_to_post(row)

    def get_post_by_date(self, start, end, source):
        rows = self.query(
            table="posts",
            where="create_time >= '%s' AND create_time <= '%s' and source in ('%s')" % (
                start, end, "','".join(source)),
            orderby="create_time"
        )
        return self._rows_to_posts(rows)

    def get_history_today(self, time_obj, source):
        import lib.timehelper as th

        dates = th.past_days(time_obj)
        posts_list = [self.get_post_by_date(d[0], d[1], source) for d in dates]

        p = {}
        for posts in posts_list:
            if posts:
                p[th.format_time(
                    timeobj=posts[0].create_time, format='%Y-%m-%d')] = posts
        return p

    def is_in_database(self, post):
        row = self.query(
            table="posts",
            where="origin_id = '%s' " % post.origin_id
        )
        return True if row else False

    def save_post(self, post):
        if not self.is_in_database(post):
            self.save(
                table="posts",
                values=post.dict
            )
        elif post.category == "rss":
            self.update(
                table="posts",
                values=post.dict,
                where="origin_id = '%s'" % post.origin_id
            )

    def delete_post(self, id):
        self.delete(
            table="posts",
            where="id=%s" % id
        )
