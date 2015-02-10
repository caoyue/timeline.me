#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import json
import datetime

from model.base import BaseModel


class Post(object):

    def __init__(self, dict):
        self.__dict__.update(dict)

    def __repr__(self):
        return repr(self.__dict__)

    __str__ = __repr__

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

        pattern = re.compile(
            """[a-zA-Z]+:\/\/[a-zA-Z0-9.]+\.[a-zA-Z0-9.\/]+""")
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

    def get_posts_count(self, source=None):
        self.count(
            "posts",
            where="source='%s'" % source if source else None
        )

    def get_posts(self, page=1, pagesize=10, source=None, orderby='create_time'):
        rows = self.query(
            table="posts",
            where="source = '%s'" % source if source else None,
            page=page,
            pagesize=pagesize
        )
        return self._rows_to_posts(rows)

    def get_posts_since(self, since_id):
        rows = self.query(
            table="posts",
            where="id > %s" % since_id if since_id else None
        )
        return self._rows_to_posts(rows)

    def get_last_post(self, source=None):
        row = self.get(
            table="posts",
            where="source = '%s'" % source if source else None,
        )
        return self._row_to_post(row)

    def is_in_database(self, post):
        row = self.query(
            table="posts",
            where="url = '%s' and origin_id = '%s' " % (
                post.url, post.origin_id)
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
