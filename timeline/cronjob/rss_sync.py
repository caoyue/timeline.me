#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from model.post import RssPost
from model.data import PostData
from utils.logger import logging
from utils.mytime import get_time_now as now

log = logging.getLogger(__file__)


def rss_sync(rss_list):
        """获取 Rss 并保存到数据库"""

        print ">> [%s]Rss Sync Start ......" % now()

        import feedparser
        for k, v in rss_list.items():
            feeds = feedparser.parse(v)
            for entry in feeds.entries:
                PostData.save_post(RssPost.status_to_post(entry, k))

        print ">> [%s]Rss Sync End." % now()
