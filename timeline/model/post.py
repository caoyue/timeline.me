#-*- coding: utf-8 -*-

import re
import json
from datetime import datetime
from config import config


class Post(object):

    def __init__(self, id, source, category, orgin_id, url, title, content, create_time, orgin_data):
        self.id = id
        self.source = source
        self.category = category
        self.orgin_id = orgin_id
        self.url = url
        self.title = title
        self.content = content
        self.create_time = create_time
        self.orgin_data = orgin_data

    @classmethod
    def replace_url(cls, content):
        """将内容中的链接文本替换成链接形式"""
        pattern = re.compile(
            """[a-zA-Z]+:\/\/[a-zA-Z0-9.]+\.[a-zA-Z0-9.\/]+""")
        matchs = pattern.findall(content)
        if matchs:
            for m in matchs:
                content = content.replace(
                    m, """<a href="%s" target="_blank">%s</a>""" % (m, m))
        return content

    @classmethod
    def status_to_post(cls, status, source):
        return status


class RssPost(Post):

    def __init__(self, id, source, orgin_id, url, title, content, create_time, orgin_data):
        super(RssPost, self).__init__(id, source, "rss",
                                      orgin_id, url, title, content, create_time, orgin_data)

    @classmethod
    def get_datetime(cls, create_time):
        return datetime(*create_time[:6])

    @classmethod
    def json_handle(cls, obj):
        def json_make_normal(obj):
            if type(obj) in [str, unicode, int, float, bool, dict, set, list, tuple]:
                return obj
            try:
                return dict(obj)
            except:
                pass
            try:
                return list(obj)
            except:
                pass
            return None
        obj = json_make_normal(obj)
        if type(obj) in [str, unicode]:
            obj = obj.replace('\\', '\\\\')
            obj = obj.replace('"', '\\"')
            obj = obj.replace('\b', '\\\b')
            obj = obj.replace('\f', '\\\f')
            obj = obj.replace('\n', '\\\n')
            obj = obj.replace('\r', '\\\r')
            obj = obj.replace('\t', '\\\t')
            return '"%s"' % obj
        elif type(obj) in [int, float]:
            return obj
        elif type(obj) is bool:
            if obj:
                return 'true'
            else:
                return 'false'
        elif type(obj) is type(None):
            return 'null'
        elif type(obj) is dict:
            temp = ''
            for key in obj.keys():
                temp += '%s:%s, ' % (
                    cls.json_handle(key), cls.json_handle(obj[key]))
            return '{\%s}' % temp[:-2]
        elif type(obj) in [set, list, tuple]:
            temp = ''
            for value in obj:
                temp += '%s, ' % cls.json_handle(value)
            return '[%s]' % temp[:-2]
        return 'null'

    @classmethod
    def status_to_post(cls, rss, source=None):
        return cls(None, source, rss.id, rss.link, rss.title, rss.summary, cls.get_datetime(rss.updated_parsed), cls.json_handle(rss))


class WeiboPost(Post):

    def __init__(self, id, orgin_id, url, title, content, create_time, orgin_data):
        super(WeiboPost, self).__init__(id, "weibo", "oauth",
                                        orgin_id, url, title, content, create_time, orgin_data)

    @classmethod
    def get_url(cls, uid, mid):
        """通过 uid 和 mid 计算该条 weibo 的 url"""
        from utils.base62 import base62_encode
        mid = str(mid)[::-1]
        size = len(mid) / 7 if len(mid) % 7 == 0 else len(mid) / 7 + 1
        result = []
        for i in range(size):
            s = mid[i * 7: (i + 1) * 7][::-1]
            s = base62_encode(int(s))
            s_len = len(s)
            if i < size - 1 and len(s) < 4:
                s = '0' * (4 - s_len) + s
            result.append(s)
        result.reverse()
        return "http://weibo.com/%s/%s" % (uid, ''.join(result))

    @classmethod
    def get_datetime(cls, create_time):
        return datetime.strptime(create_time, '%a %b %d %H:%M:%S +0800 %Y')

    @classmethod
    def status_to_post(cls, status, source=None):
        content = cls.replace_url(status.text)
        if status.pic_urls:
            for pic in status.pic_urls:
                content += """  <a href="%s" target="_blank">pic</a>""" % pic[
                    "thumbnail_pic"].replace("thumbnail", "large")
        if "retweeted_status" in status:
            retweet_content = cls.replace_url(status.retweeted_status.text)
            if status.retweeted_status.pic_urls:
                for pic in status.retweeted_status.pic_urls:
                    retweet_content += """  <a href="%s" target="_blank">pic</a>""" % pic[
                        "thumbnail_pic"].replace("thumbnail", "large")
            content += " <blockquote>@%s:%s</blockquote>" % (
                status.retweeted_status.user.screen_name, retweet_content)
        return cls(None, status.id, cls.get_url(status.user.id, status.mid), status.text, content, cls.get_datetime(status.created_at), status)


class TwitterPost(Post):

    def __init__(self, id, orgin_id, url, title, content, create_time, orgin_data):
        super(TwitterPost, self).__init__(id, "twitter", "oauth",
                                          orgin_id, url, title, content, create_time, orgin_data)

    @classmethod
    def get_url(cls, status_id, name):
        return "http://twitter.com/%s/status/%s" % (name, status_id)

    @classmethod
    def get_datetime(cls, create_time):
        return datetime.strptime(create_time, '%a %b %d %H:%M:%S +0000 %Y')

    @classmethod
    def status_to_post(cls, status, source=None):
        content = status["text"]
        if "retweeted_status" in status:
            content = "%s <blockquote>@%s:%s</blockquote>" % (
                status["text"], status["retweeted_status"]["user"]["screen_name"], status["retweeted_status"]["text"])
        return cls(None, status["id"], cls.get_url(status["id"], status["user"]["name"]), status["text"], cls.replace_url(content), cls.get_datetime(status["created_at"]), json.dumps(status))
