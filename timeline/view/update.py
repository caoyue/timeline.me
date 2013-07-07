#-*- coding: utf-8 -*-

from .base import LoginBase


class index(LoginBase):

    def GET(self):
        return "test"
