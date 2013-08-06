#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("../timeline/")

from search.creater import create_index
from config.config import SEARCH_INDEX_PATH as index_path

if __name__ == '__main__':
    create_index(index_path, False)
