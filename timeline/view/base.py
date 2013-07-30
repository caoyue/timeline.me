#-*- coding: utf-8 -*-

import web
from web.contrib.template import render_jinja
from model.login import Login
from config import config


class Base(object):

    site = config.SITE

    render = render_jinja(config.RENDER_PATH,  encoding='utf-8')

    render._lookup.globals.update(
        site=config.SITE,
        links=config.LINKS,
        source=config.FEEDS_DICT.keys() + config.OAUTH_DICT.keys()
    )


class LoginBase(Base):

    def __init__(self):
        if not Login.is_logged():
            raise web.seeother("/login")
