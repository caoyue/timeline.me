#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import json
from api.twitter import TwitterOauth
from model.post import TwitterPost
from model.data import PostData
from model.data import ConfigData
from utils.logger import logging
from utils.mytime import get_time_now as now

log = logging.getLogger(__file__)


def twitter_sync(twitter_config):
    """获取 tweets 并保存到数据库"""

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

    since_id = None
    last_post = PostData.get_last_post("twitter")
    if last_post:
        since_id = last_post.orgin_id

    try:
        client = TwitterOauth(twitter_config, twitter_access)
        status = client.get_user_timeline(since_id=since_id)
    except Exception, e:
        print ">> [error] get timeline failed , task break: %s" % e
        log.warning("%s" % e)
        print ">> [%s]Twitter Sync End." % now()
        return

    for s in status:
        PostData.save_post(TwitterPost.status_to_post(s))

    print ">> [%s]Twitter Sync End." % now()
