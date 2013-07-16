#-*- coding: utf-8 -*-

import time
import datetime


def get_time():
    return datetime.datetime.now()


def get_time_now(format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format, time.localtime(time.time()))


def get_time_from_string(time_str, format='%Y-%m-%d'):
    return datetime.datetime.strptime(time_str, format)
