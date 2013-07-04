#!/usr/bin/env python
#-*- coding: utf-8 -*-

import web
import config.routes

app = web.application(config.routes.urls, globals())
# application = app.wsgifunc()

if __name__ == '__main__':
    app.run()
