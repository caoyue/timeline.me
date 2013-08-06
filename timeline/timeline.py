#!/usr/bin/env python
#-*- coding: utf-8 -*-

import web
from config import routes

from view.error import Error


app = web.application(routes.urls, globals())
app.notfound = Error.notfound

application = app.wsgifunc()
