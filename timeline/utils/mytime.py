#-*- coding: utf-8 -*-

import datetime


def get_time():
    return datetime.datetime.now()


def get_time_now(format='%Y-%m-%d %H:%M:%S'):
    return get_time().strftime(format)


def get_time_from_string(time_str, format='%Y-%m-%d'):
    return datetime.datetime.strptime(time_str, format)


def get_yesterday(now=None, format="%Y-%m-%d"):
    if not now:
        now = get_time()
    return (now + datetime.timedelta(days=-1)).strftime(format)


def get_tomorrow(now=None, format="%Y-%m-%d"):
    if not now:
        now = get_time()
    return (now + datetime.timedelta(days=1)).strftime(format)
