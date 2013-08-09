#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("../timeline/")

from search.creater import create_index
from config import config

if __name__ == '__main__':
    create_index(config.SEARCH_INDEX_PATH, config.SEARCH_DICT_PATH, False)
