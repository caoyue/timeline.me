#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json

from lib.db import Commander


class BaseModel(Commander):

    def __init__(self, db):
        self.connection = db
        super(BaseModel, self).__init__()

    # function

    def get_config_time(self, name):
        value = self.get(
            table="configs",
            fields=["value, create_time"],
            where="name = '%s'" % name
        )
        if value:
            return {
                "value": json.loads(value["value"]),
                "create_time": value["create_time"]
            }

        return None

    def get_config(self, name):
        value = self.get_config_time(name)
        return value["value"] if value else None

    def replace_config(self, name, values):
        from lib.timehelper import format_now

        value = json.dumps(values)
        return self.replace(
            table="configs",
            values={
                "name": name,
                "value": value,
                "create_time": format_now(format="%Y-%m-%d %H:%M:%S")
            }
        )
