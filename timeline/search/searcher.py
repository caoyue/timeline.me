# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import MultifieldParser
# from whoosh import highlight

import jieba

from config import config
from model.post import Post

import time


def search_page(keyword, page=1, pagesize=10):
    index_path = config.SEARCH_INDEX_PATH
    dict_path = config.SEARCH_DICT_PATH
    if not os.path.exists(index_path):
        raise IOError, "index path [%s] not exists!" % index_path

    if dict_path:
        jieba.set_dictionary(dict_path)

    ix = open_dir(index_path)

    t1 = time.time()
    parser = MultifieldParser(["content_text", "title"], schema=ix.schema)
    q = parser.parse(keyword)

    posts = []
    with ix.searcher() as searcher:

        results = searcher.search(
            q, limit=page * pagesize, sortedby="create_time", reverse=True, terms=True)

        # results.fragmenter = highlight.WholeFragmenter(charlimit=32768)
        # results.formatter = highlight.HtmlFormatter(
        #     tagname="span", classname="match", termclass="term")
        for hit in results[(page - 1) * pagesize:page * pagesize]:
            posts.append(search_to_post(hit, keyword))

        terms = '|'.join(
            set([x[1].decode('utf-8') for x in results.matched_terms()]))

    return {"posts": posts, "terms": terms, "length": results.estimated_length(), "time": time.time() - t1}


def search_to_post(hit, keyword):
    post = Post()
    for k in hit.keys():
        if k != "content_text":
            setattr(post, k, hit[k])
    return post
