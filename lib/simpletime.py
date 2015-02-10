#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime


def get_time(time_str, format='%Y-%m-%d', timezone=8):
    """
    china: timezone = 8
    format: 'Tue May 31 17:46:55 +0800 2011' - '%a %b %d %H:%M:%S +0800 %Y'
    """
    return datetime.datetime.strptime(time_str, format) + \
        datetime.timedelta(seconds=(timezone - 8) * 3600)


def get_time_now(format='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.now().strftime(format)


def get_yesterday(now=None, format="%Y-%m-%d"):
    if not now:
        now = get_time()
    return (now + datetime.timedelta(days=-1)).strftime(format)


def get_tomorrow(now=None, format="%Y-%m-%d"):
    if not now:
        now = get_time()
    return (now + datetime.timedelta(days=1)).strftime(format)
