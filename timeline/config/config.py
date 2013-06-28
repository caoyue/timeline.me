#-*- coding: utf-8 -*-

# mysql setting
DB_HOST = ""
DB_PORT = 3306
DB_NAME = ""
DB_USR = ""
DB_PSW = ""

# site
SITE = {
    "domain": "",
    "title": u"",
    "description": u"",
    "author": ""
}

# my links
LINKS = [
    {
        "name": "",
        "title": "",
        "link": ""
    },
    {
        "name": "",
        "title": "",
        "link": ""
    },
    {
        "name": "",
        "title": "",
        "link": ""
    },
    {
        "name": "",
        "title": "",
        "link": ""
    },
    {
        "name": "",
        "title": "",
        "link": ""
    }
]


# pagesize
PAGESIZE = 10

# template render
RENDER_PATH = "templates"

# log file path
LOG_PATH_NAME = "mytimeline.log"

# category
CATEGORY_DICT = {
    "rss": "rss",
    "oauth": "oauth"
}

# feeds
FEEDS_DICT = {
    "blog": ""
}

# oauth
OAUTH_DICT = {
    "weibo": {
        "app_name": "weibo",
        "app_key": "",
        "app_secret": "",
        "redirect_uri": SITE["domain"] + "/weibo/callback"
    },
    "twitter": {
        "app_name": "twitter",
        "consumer_key": "",
        "consumer_secret": "",
        "redirect_uri": SITE["domain"] + "/twitter/callback",
        "request_token_url": "https://api.twitter.com/oauth/request_token",
        "authorize_url ": "https://api.twitter.com/oauth/authorize",
        "access_token_url": "https://api.twitter.com/oauth/access_token"
    }
}

source_filter = '|'.join(FEEDS_DICT.keys() + OAUTH_DICT.keys())
