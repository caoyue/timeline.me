#-*- coding: utf-8 -*-

import web
from search.searcher import search_page as s
from .base import Base


class index(Base):

    def GET(self, keyword):
        results = s(keyword)

        return self.render.index(
            posts=results["posts"], title=self.site["title"],
            pager=None, search=keyword, terms=results["terms"])

    def POST(self):
        data = web.input()
        return web.seeother("/search/%s" % data.keyword)
