#-*- coding: utf-8 -*-

from .base import Base


class index(Base):

    def GET(self):
        return self.render.login()
