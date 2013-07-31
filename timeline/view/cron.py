#!/usr/bin/env python
#-*- coding: utf-8 -*-

from .base import LoginBase
from cronjob.sync_timeline import sync_timeline
from cronjob.statistics import statistics


class index(LoginBase):

    def GET(self, *cron):
        message = None
        if cron:
            if cron[0] == "timeline":
                sync_timeline()
                message = ">> Sync timeline Success!"
            elif cron[0] == "statistic":
                statistics()
                message = ">> Success!"
            else:
                message = "cronjob not found!"
        return self.render.cron(message=message, title="Cron - %s" % self.site["title"])
