#!/usr/bin/env python
# -*- coding: utf-8 -*-


from handler.base import BaseHandler


class IndexHandler(BaseHandler):

    def get(self, source="timeline", page=None):
        from lib.pager import Pager

        if source not in self.source and source != "timeline":
            self.raise_error(404)

        _p = int(page) if page else 1
        pagesize = self.config.site["pagesize"]
        posts = self.posts.get_posts(
            page=_p, pagesize=pagesize, source=source)

        new_posts = []
        for post in posts:
            post.source += "|"
            post.duplicate = False
            for new in new_posts:
                if post.is_duplicate(new):
                    new.source += post.source + "|"
                    post.duplicate = True
            new_posts.append(post)

        pager = Pager(
            self.posts.get_posts_count(source=source), pagesize, _p, "/%s/" % source)
        self.render("index.html", posts=new_posts, pager=pager, title=source)


class PingHandler(BaseHandler):

    def get(self):
        self.write("pong!")


class NotFoundHandler(BaseHandler):

    def get(self):
        self.render("404.html", title="404")
