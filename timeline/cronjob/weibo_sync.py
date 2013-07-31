#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import json
from api.weibo import WeiboOauth
from model.post import WeiboPost
from model.data import PostData
from model.data import ConfigData
from utils.logger import logging
from utils.mytime import get_time_now as now

log = logging.getLogger(__file__)


def weibo_sync(weibo_config):
        """获取 weibo 并保存到数据库"""

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

        since_id = None
        last_post = PostData.get_last_post("weibo")
        if last_post:
            since_id = last_post.orgin_id

        try:
            client = WeiboOauth(weibo_config, weibo_access)
            status = client.get_user_timeline(since_id=since_id)
        except Exception, e:
            print ">> [error] get timeline failed , task break：%s" % e
            log.warning("%s" % e)
            print ">> [%s]Weibo Sync End." % now()
            return

        for s in status.statuses:
            PostData.save_post(WeiboPost.status_to_post(s))

        print ">> [%s]Get %s statuses" % (now(), len(status.statuses))
        print ">> [%s]Weibo Sync End." % now()
        print "---------------"
