#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import time
import datetime


class DateEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, time.struct_time):
            return time.strftime('%Y-%m-%d %H:%M:%S', obj)
        else:
            return json.JSONEncoder.default(self, obj)
