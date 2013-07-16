#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import json
from api.weibo import WeiboOauth
from model.post import WeiboPost
from api.twitter import TwitterOauth
from model.post import TwitterPost
from model.data import PostData
from model.data import ConfigData
from utils.logger import logging
from utils.mytime import get_time_now as now

log = logging.getLogger(__file__)


def weibo(weibo_config):
    """获取全部微博并保存到数据库"""

    print ">> [%s]Weibo Sync Start ...... " % now()

    config_string = ConfigData.get_config_value("weibo_access_token")
    weibo_access = None
    if config_string:
        try:
            weibo_access = json.loads(config_string)
        except Exception, e:
            print ">> [error] decode config value failed ,task break: %s" % e
            log.warning("%s" % e)
            print ">> [%s]Weibo Sync End." % now()
            return
    else:
        print ">> [error] weibo config is null, task break."
        print ">> [%s]Weibo Sync End." % now()
        return

    client = None
    try:
        client = WeiboOauth(weibo_config, weibo_access)
    except Exception, e:
        print ">> [error] get timeline failed , task break：%s" % e
        return

    i = 1
    count = 0
    while True:
        status = client.get_user_timeline_by_page(count=100, page=i)

        if not status.statuses:
            break

        for s in status.statuses:
            PostData.save_post(WeiboPost.status_to_post(s))

        count += len(status.statuses)
        i += 1

    print ">> [%s]Weibo Sync End." % now()
    print ">> [%s]Total weibo count %s" % (now(), count)


def twitter(twitter_config):
    """获取所有 Tweets 并保存到数据库"""

    print ">> [%s]Twitter Sync Start ...... " % now()

    config_string = ConfigData.get_config_value("twitter_access_token")
    twitter_access = None
    if config_string:
        try:
            twitter_access = json.loads(config_string)
        except Exception, e:
            print ">> [error] decode config value failed ,task break: %s" % e
            log.warning("%s" % e)
            print ">> Twitter Sync End."
            return
    else:
        print ">> [error] twitter config is null, task break."
        print ">> [%s]Twitter Sync End." % now()
        return

    client = None
    try:
        client = TwitterOauth(twitter_config, twitter_access)
    except Exception, e:
        print ">> [error] get timeline failed , task break: %s" % e
        log.warning("%s" % e)
        print ">> [%s]Twitter Sync End." % now()
        return

    alltweets = []
    new_tweets = client.get_user_timeline(count=200)
    alltweets.extend(new_tweets)

    # 保存最大 id - 1
    oldest = alltweets[-1]["id"] - 1

    while len(new_tweets) > 0:
        print ">> [%s]获取从 %s 开始的 Twitter" % (now(), oldest)

        new_tweets = client.get_user_timeline(count=200, max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1]["id"] - 1
        print ">> 已获取 %s 条 Tweets" % (len(alltweets))

    print ">> 保存到数据库……"
    for t in alltweets:
        PostData.save_post(TwitterPost.status_to_post(t))

    print ">> [%s]Twitter Sync End." % now()
    print ">> [%s]Total tweets count %s." % (now(), len(alltweets))
