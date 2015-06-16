#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model.post import PostModel


class OauthModel(PostModel):

    def __init__(self, db):
        super(OauthModel, self).__init__(db)

    # function

    def save_access_token(self, name, values):
        self.replace_config(name, values)

    def get_access_token(self, name):
        return self.get_config(name)

    def save_request_token(self, name, values):
        self.replace_config("%s_request_token" % name, values)

    def get_request_token(self, name):
        return self.get_config("%s_request_token" % name)

    def binded_accounts(self, oauth):
        l = []
        for a in oauth:
            if self.get_access_token(a):
                l.append(a)

        return l
