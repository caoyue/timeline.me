#!/usr/bin/env python
# -*- coding: utf-8 -*-


# mysql setting
mysql = {
    "host": "127.0.0.1",
    "port": 3306,
    "database": "timeline",
    "user": "root",
    "password": ""
}

# site
site = {
    "domain": "http://example.me",
    "title": u"site title",
    "description": u"site description",
    "author": u"",
    "pagesize": 10,
    "tzinfo": 'Asia/Shanghai'
}

# secret
secret = "MmMxM2I5NGEyNTk0ODBiM2RmOWRmNGZmMDJhNjdkMTM="

# feeds
feeds = {
    "blog": "http://blog.example.me/feed"
}

# oauth
oauth = {
    "weibo": {
        "app_name": "weibo",
        "app_key": "",
        "app_secret": "",
        "redirect_uri": site["domain"] + "/weibo/callback"
    },
    "twitter": {
        "app_name": "twitter",
        "consumer_key": "",
        "consumer_secret": "",
        "redirect_uri": site["domain"] + "/twitter/callback",
        "request_token_url": "https://api.twitter.com/oauth/request_token",
        "authorize_url ": "https://api.twitter.com/oauth/authorize",
        "access_token_url": "https://api.twitter.com/oauth/access_token"
    }
}

# sidebar links
links = [
    {
        "name": "example",
        "title": "an example",
        "link": "http://example.com/xxxx"
    },
    {
        "name": "",
        "title": "",
        "link": ""
    }
]
