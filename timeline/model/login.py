#-*- coding: utf-8 -*-

import web
import hashlib
from config import config


class Login(object):

    @classmethod
    def get_account_str(cls):

        def sha1(str):
            h = hashlib.sha1()
            h.update(str)
            return h.hexdigest()
        return sha1(config.SITE["author"] + config.SALT + web.ctx.ip)

    @classmethod
    def login(cls):
        web.setcookie('tm', cls.get_account_str(), expires=3600 * 24 * 7)

    @classmethod
    def logout(cls):
        web.setcookie('tm', "", expires=-1)

    @classmethod
    def is_logged(cls):
        cookie = web.cookies().get("tm")
        if cookie == cls.get_account_str():
            return True
        cls.logout()
        return False
