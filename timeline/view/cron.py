#!/usr/bin/env python
#-*- coding: utf-8 -*-

from cronjob.jobs import run_jobs
from .base import LoginBase


class jobs(LoginBase):

    def GET(self):
        try:
            run_jobs()
        except Exception:
            return "Failed!"
        else:
            return "Success!"
