#!/usr/bin/env python
# -*- coding: utf-8 -*-


from model.post import Post, PostModel
from lib.timehelper import format_now as now, format_timestr


class WeiboModel(PostModel):

    def __init__(self, db):
        super(WeiboModel, self).__init__(db)

    # function

    def get_url(self, uid, mid):
        """calculates url by uid and mid"""

        from lib.base62 import base62_encode
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

    def status_to_post(self, status, source=None):
        def not_deleted(status):
            if hasattr(status, "deleted") and status.deleted == "1":
                return False
            return True
        content = self.replace_url(status.text)
        # contains pics
        if not_deleted(status) and status.pic_urls:
            for pic in status.pic_urls:
                content += """  <a href="%s" target="_blank">pic</a>""" % pic[
                    "thumbnail_pic"].replace("thumbnail", "large")

        # contains retweet
        if "retweeted_status" in status:
            # tweet deleted
            if not_deleted(status.retweeted_status):
                retweet_content = self.replace_url(
                    status.retweeted_status.text)
                if status.retweeted_status.pic_urls:
                    for pic in status.retweeted_status.pic_urls:
                        retweet_content += """  <a href="%s" target="_blank">pic</a>""" % pic[
                            "thumbnail_pic"].replace("thumbnail", "large")
                content += " <blockquote>@%s:%s</blockquote>" % (
                    status.retweeted_status.user.screen_name, retweet_content)
            else:
                content += "<blockquote>%s</blockquote>" % status.retweeted_status.text

        return Post({
            "source": "weibo",
            "category": "oauth",
            "origin_id": str(status.id),
            "url": self.get_url(status.user.id, status.mid),
            "title": status.text,
            "content": content,
            "create_time": format_timestr(status.created_at),
            "origin_data": status
        })

    def sync(self, client):
        """sync tweets"""

        print ">> [%s]Weibo Sync Start ...... " % now()

        try:
            since_id = None
            last_post = self.get_last_post("weibo")
            if last_post:
                since_id = last_post.origin_id

            status = client.get_user_timeline(since_id=since_id)
            print ">> [%s]Get %s statuses, saving ..." % (now(), len(status.statuses))

            for s in status.statuses:
                self.save_post(self.status_to_post(s))
        except Exception, e:
            print e
            print ">> Error!"

        print ">> [%s]Weibo Sync End." % now()
        print "---------------"

    def sync_all(self, client):
        """Get all tweets
        maybe takes a long time if you have many tweets
        """

        print ">> [%s]Weibo Sync Start ...... " % now()

        try:
            i = 1
            count = 0
            while True:
                status = client.get_user_timeline_by_page(count=100, page=i)

                if not status.statuses:
                    break

                for s in status.statuses:
                    self.save_post(self.status_to_post(s))

                count += len(status.statuses)
                i += 1
        except Exception, e:
            print e
            print ">> Error!"

        print ">> [%s]Total weibo count %s" % (now(), count)
        print ">> [%s]Weibo Sync End." % now()
        print "---------------"
