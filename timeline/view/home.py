#-*- coding: utf-8 -*-

import web
from config import config
from model.data import PostData
from model.pager import Pager
from .base import Base


class index(Base):

    def GET(self, *page):
        _p = 1
        try:
            _p = int(page[0])
        except Exception:
            _p = 1
        posts = PostData.get_posts(_p, config.PAGESIZE)
        pager = Pager(PostData.get_posts_count(), config.PAGESIZE, _p, "/")
        if not posts and pager.posts_count:
            raise web.seeother("/1")

        new_posts = []
        for post in posts:
            post.source += "|"
            post.duplicate = False
            for new in new_posts:
                if post.is_duplicate(new):
                    new.source += post.source + "|"
                    post.duplicate = True
            new_posts.append(post)
        return self.render.index(posts=new_posts, pager=pager, title=config.SITE["title"])


class source(Base):

    def GET(self, source, *page):
        _p = 1
        try:
            _p = int(page[0])
        except Exception:
            _p = 1
        posts = PostData.get_source_posts(source, _p, config.PAGESIZE)
        pager = Pager(PostData.get_posts_count(
            source), config.PAGESIZE, _p, "/%s/" % source)
        return self.render.index(posts=posts, pager=pager, title=source + " - " + config.SITE["title"])


class feed(Base):

    def GET(self):
        posts = PostData.get_posts(1, 20)
        web.header('Content-Type', 'text/xml')
        return self.render.feed(posts=posts, domain=config.SITE["domain"])
