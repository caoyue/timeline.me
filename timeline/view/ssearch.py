#-*- coding: utf-8 -*-

import web
from search.searcher import search_page as s
from .base import Base
from model.pager import Pager


class index(Base):

    def GET(self, keyword, *page):
        pagesize = 10
        _p = 1
        if page and int(page[0]) > 0:
            _p = int(page[0])

        results = s(keyword, _p, pagesize)

        pager = Pager(results["length"], pagesize, _p, "/search/%s/" % keyword)

        return self.render.index(
            posts=results["posts"], title=self.site["title"],
            pager=pager, search=keyword, terms=results["terms"], count=results["length"], time=results["time"])

    def POST(self):
        data = web.input()
        return web.seeother("/search/%s" % data.keyword)
