#-*- coding: utf-8 -*-

import web
from .base import Base
from utils.mobile import is_mobile_browser as im


class Error(Base):

    @classmethod
    def notfound(cls):
        if im(web.ctx.env['HTTP_USER_AGENT']):
            return web.notfound("Not Found")
        return web.notfound(cls.render.notfound(title="NotFound"))

    @classmethod
    def internalerror(cls):
        return web.internalerror("Bad, bad server. No donut for you.")
