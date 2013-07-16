#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

sys.path.append("../timeline/")
from cronjob import first_sync
from config import config

if __name__ == '__main__':
    first_sync.weibo(config.OAUTH_DICT["weibo"])
    first_sync.Twitter(config.OAUTH_DICT["twitter"])
