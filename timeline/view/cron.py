#!/usr/bin/env python
#-*- coding: utf-8 -*-

from cronjob.jobs import run_jobs


class jobs(object):

    def GET(self):
        ex = None
        try:
            run_jobs()
        except Exception, e:
            return ex
        else:
            return "Success!"

if __name__ == '__main__':
    run_jobs()
