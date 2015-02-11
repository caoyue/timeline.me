#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Pager(object):

    def __init__(self, posts_count, pagesize, current_page, page_url):
        self.posts_count = posts_count
        self.total_page = self.posts_count / pagesize + 1 \
            if self.posts_count % pagesize else self.posts_count / pagesize
        self.current_page = current_page
        self.next_page = self.current_page + 1 \
            if self.current_page < self.total_page else 0
        self.previous_page = self.current_page - 1 \
            if self.current_page > 1 else 0
        self.next_page_url = page_url + str(self.next_page)
        self.previous_page_url = page_url + str(self.previous_page)
