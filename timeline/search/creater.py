# -*- coding: UTF-8 -*-

import os
from whoosh.index import create_in
from whoosh.fields import *

from jieba.analyse import ChineseAnalyzer

from model.data import PostData as p
from model.data import ConfigData as c
from utils.mytime import get_time_now as now


def create_index(index_path, clean=False):

    print ">> [%s]Indexing......" % now()
    print ">> Index Mode : %s" % ("Clean" if clean else "Incremental")
    analyzer = ChineseAnalyzer()

    schema = Schema(
        id=NUMERIC(stored=True, unique=True),
        source=TEXT(stored=True),
        category=TEXT(stored=True),
        origin_id=TEXT(stored=True),
        url=TEXT(stored=True),
        title=TEXT(stored=True, analyzer=analyzer),
        content_text=TEXT(stored=True, analyzer=analyzer),
        content=TEXT(stored=True),
        create_time=DATETIME(stored=True)
    )
    if not os.path.exists(index_path):
        os.mkdir(index_path)

    ix = create_in(index_path, schema)
    writer = ix.writer()

    count = 0
    last_index_id = c.get_config_value("last_index_id")
    if last_index_id and not clean:
        posts = p.get_posts_since(last_index_id)
        add_docs(writer, posts)
        count += len(posts)
    else:
        page = 1
        while True:
            posts = p.get_posts(page=page, pagesize=30)
            if posts:
                add_docs(writer, posts)
                page += 1
                count += len(posts)
            else:
                break

    writer.commit()

    last_index = p.get_posts(1, 1, 'id')[0]
    c.set_config_value("last_index_id", last_index.id)

    print ">> Index to id %s,{ title : %s}" % (last_index.id, last_index.title)
    print ">> Indexed %s items" % count
    print ">> [%s]Indexed End." % now()
    print "---------------"


def add_docs(writer, posts):
    for post in posts:
        writer.add_document(
            id=post.id,
            source=post.source,
            category=post.category,
            origin_id=post.origin_id,
            url=post.url,
            title=post.title,
            content_text=html_strip(post.content),
            content=post.content,
            create_time=post.create_time
        )


def html_strip(html):
    """ get text from html """
    from HTMLParser import HTMLParser
    html = html.strip()
    html = html.strip("\n")

    result = []
    parse = HTMLParser()
    parse.handle_data = result.append
    parse.feed(html)
    parse.close()

    return "".join(result)
