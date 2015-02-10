#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json

from model.post import Post, PostModel
from lib.simpletime import get_time_now as now, get_time


class TwitterModel(PostModel):

    def __init__(self, db):
        super(TwitterModel, self).__init__(db)

    # function

    def get_url(self, status_id, name):
        return "http://twitter.com/%s/status/%s" % (name, status_id)

    def status_to_post(self, status, source=None):
        content = status["text"]
        # contains retweet
        if "retweeted_status" in status:
            content = "%s <blockquote>@%s:%s</blockquote>" % (
                status["text"], status["retweeted_status"]["user"]["screen_name"], status["retweeted_status"]["text"])

        from config import site

        return Post({
            "source": "twitter",
            "category": "oauth",
            "origin_id": str(status["id"]),
            "url": self.get_url(status["id"], status["user"]["name"]),
            "title": status["text"],
            "content": self.replace_url(content),
            "create_time": str(get_time(
                status["created_at"], '%a %b %d %H:%M:%S +0000 %Y', site["timezone"])),
            "origin_data": json.dumps(status)
        })

    def sync(self, client):
        """sync tweets"""

        print ">> [%s]Twitter Sync Start ...... " % now()

        since_id = None
        last_post = self.get_last_post("twitter")
        if last_post:
            since_id = last_post.origin_id

        print ">> [%s]Getting tweets since %s ..." % (now(), since_id)
        status = client.get_user_timeline(since_id=since_id)

        print ">> [%s]Got %s tweets, saving..." % (now(), len(status))
        for s in status:
            self.save_post(self.status_to_post(s))

        print ">> [%s]Twitter Sync End." % now()
        print "---------------"

    def sync_all(self, client):
        """Get all tweets
        maybe takes a long time if you have many tweets
        """

        print ">> [%s]Twitter Sync Start ...... " % now()

        alltweets = []
        new_tweets = client.get_user_timeline(count=200)
        alltweets.extend(new_tweets)

        # 保存最大 id - 1
        oldest = alltweets[-1]["id"] - 1

        while len(new_tweets) > 0:
            print ">> [%s]Getting tweets since %s ..." % (now(), oldest)

            new_tweets = client.get_user_timeline(count=200, max_id=oldest)
            alltweets.extend(new_tweets)
            oldest = alltweets[-1]["id"] - 1
            print ">> Got %s tweets, saving..." % (len(alltweets))

        for t in alltweets:
            self.save_post(self.status_to_post(t))

        print ">> [%s]Total tweets count : %s." % (now(), len(alltweets))
        print ">> [%s]Twitter Sync End." % now()
        print "---------------"
