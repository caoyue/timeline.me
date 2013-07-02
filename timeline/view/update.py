#-*- coding: utf-8 -*-

import web
from .base import LoginBase


class index(LoginBase):

    def GET(self):
        return "test"
