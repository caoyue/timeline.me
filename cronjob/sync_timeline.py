#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

sys.path.append("../timeline/")
from cronjob.sync_timeline import sync_timeline

if __name__ == '__main__':
    sync_timeline()
