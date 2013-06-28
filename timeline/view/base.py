#-*- coding: utf-8 -*-

from web.contrib.template import render_jinja
from config import config


class Base(object):

    render = render_jinja(config.RENDER_PATH,  encoding='utf-8')

    render._lookup.globals.update(
        site=config.SITE,
        links=config.LINKS,
        source=config.FEEDS_DICT.keys() + config.OAUTH_DICT.keys()
    )
