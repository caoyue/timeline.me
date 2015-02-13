#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime


def now():
    return datetime.datetime.now()


def parse_timestr(timestr, parse="%Y-%m-%d", timezone=8):
    """
    china: timezone = 8
    format: 'Tue May 31 17:46:55 +0800 2011' - '%a %b %d %H:%M:%S +0800 %Y'
    """
    return datetime.datetime.strptime(timestr, parse) + \
        datetime.timedelta(seconds=(timezone - 8) * 3600)


def format_time(timeobj, format='%Y-%m-%d', timezone=8):
    return (timeobj + datetime.timedelta(seconds=(timezone - 8) * 3600)).strftime(format)


def format_now(format='%Y-%m-%d %H:%M:%S'):
    return format_time(now(), format=format)


def format_timestr(timestr, parse="%Y-%m-%d", format='%Y-%m-%d', parse_timezone=8, timezone=8):
    return format_time(
        timeobj=parse_timestr(
            timestr=timestr, parse=parse, parse_timezone=timezone),
        format=format, timezone=timezone)


def format_day_ago(timeobj=None, days=0, format="%Y-%m-%d"):
    timeobj = timeobj if timeobj else now()
    return format_time(timeobj + datetime.timedelta(days=days), format=format)


def past_days(timeobj=None):
    timeobj = timeobj if timeobj else now()
    years = range(timeobj.year - 1, 2005, -1)
    return [("%s-%s" % (y, format_time(timeobj, format="%m-%d")),
             "%s-%s" % (y, format_day_ago(timeobj=timeobj, days=1, format="%m-%d")))
            for y in years]
