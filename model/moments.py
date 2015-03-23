#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json

from model.post import Post, PostModel
from lib.timehelper import format_now as now


class MomentsModel(PostModel):

    def __init__(self, db):
        super(MomentsModel, self).__init__(db)

    # function

    def status_to_post(self, status, source=None):
        import hashlib

        return Post({
            "source": "moments",
            "category": "moments",
            "origin_id": "moments:%s" % hashlib.md5(status).hexdigest(),
            "url": "",
            "title": status,
            "content": self.replace_url(status),
            "create_time": now(),
            "origin_data": status
        })

    def compose(self, status):
        self.save_post(self.status_to_post(status))
