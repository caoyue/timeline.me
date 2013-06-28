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

log = logging.getLogger(__file__)


def weibo_sync(weibo_config):
        """获取 weibo 并保存到数据库"""

        print ">> Weibo Sync Start ...... "

        config_string = ConfigData.get_config_value("weibo_access_token")
        weibo_access = None
        if config_string:
            try:
                weibo_access = json.loads(config_string)
            except Exception, e:
                print ">> [error] decode config value failed ,task break"
                log.warning("%s" % e)
                print ">> Weibo Sync End."
                return
        else:
            print ">> [error] weibo config is null, task break"
            print ">> Weibo Sync End."
            return

        try:
            client = WeiboOauth(weibo_config, weibo_access)
            status = client.get_user_timeline()
        except Exception, e:
            print ">> [error] get timeline failed , task break"
            log.warning("%s" % e)
            print ">> Weibo Sync End."
            return

        for s in status.statuses:
            PostData.save_post(WeiboPost.status_to_post(s))

        print ">> Weibo Sync End."
