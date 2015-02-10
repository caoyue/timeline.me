#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json

from lib.db import Commander


class BaseModel(Commander):

    def __init__(self, db):
        self.db = db
        super(BaseModel, self).__init__()

    # function

    def get_config(self, name):
        config_value = self.get(
            table="configs",
            fields=["value"],
            where="name = '%s'" % name
        )
        if config_value:
            return json.loads(config_value["value"])

        return None

    def replace_config(self, name, values):
        value = json.dumps(values)
        return self.replace(
            table="configs",
            values={"name": name, "value": value}
        )
