# -*- coding: UTF-8 -*-

import os
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import MultifieldParser
from whoosh import highlight

from config.config import SEARCH_INDEX_PATH as index_path
from model.post import Post


def search_page(keyword, page=1, pagesize=10):

    if not os.path.exists(index_path):
        raise IOError, "index path [%s] not exists!" % index_path

    ix = open_dir(index_path)
    parser = MultifieldParser(["content_text", "title"], schema=ix.schema)
    q = parser.parse(keyword)

    posts = []
    with ix.searcher() as searcher:

        results = searcher.search(
            q, sortedby="create_time", reverse=True, terms=True)

        results.fragmenter = highlight.WholeFragmenter(charlimit=32768)
        # results.formatter = highlight.HtmlFormatter(
        #     tagname="span", classname="match", termclass="term")
        for hit in results:
            posts.append(search_to_post(hit, keyword))

        terms = '|'.join(
            set([x[1].decode('utf-8') for x in results.matched_terms()]))

    return {"posts": posts, "terms": terms}


def search_to_post(hit, keyword):
    post = Post()
    for k in hit.keys():
        if k != "content_text":
            setattr(post, k, hit[k])
    return post
