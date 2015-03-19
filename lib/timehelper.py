#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
from dateutil import parser, tz, rrule
from config import site


def parse_timestr(timestr):
    return parser.parse(timestr)


def now(tzinfo=site["tzinfo"]):
    return datetime.datetime.now(tz.gettz(tzinfo))


def to_local(timeobj, tzinfo=site["tzinfo"]):
    """convert timeobj to local time
    if timeobj have no tzinfo, use tzlocal instead
    """
    t = timeobj
    if not timeobj.tzinfo:
        t = timeobj.replace(tzinfo=tz.tzlocal())

    return t.astimezone(tz.gettz(tzinfo))


def format_time(timeobj, format='%Y-%m-%d %H:%M:%S'):
    return timeobj.strftime(format)


def format_now(format='%Y-%m-%d %H:%M:%S', tzinfo=site["tzinfo"]):
    return format_time(now(tzinfo), format)


def format_timestr(timestr, format='%Y-%m-%d %H:%M:%S', tzinfo=site["tzinfo"]):
    parsed_time = parse_timestr(timestr)
    local_time = to_local(parsed_time, tzinfo)
    return format_time(local_time, format=format)


def format_day_ago(timeobj=None, days=0, format="%Y-%m-%d"):
    timeobj = timeobj if timeobj else now()
    return format_time(timeobj + datetime.timedelta(days=days), format=format)


def past_days(timeobj=None):
    timeobj = to_local(timeobj) if timeobj else now()
    years = range(timeobj.year - 1, 2005, -1)
    return [("%s-%s" % (y, format_time(timeobj, format="%m-%d")),
             "%s-%s" % (y, format_day_ago(timeobj=timeobj, days=1, format="%m-%d")))
            for y in years]


def datediff(start, end):
    return rrule.rrule(rrule.DAILY, dtstart=start, until=end).count()
