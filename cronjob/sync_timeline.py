#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

sys.path.append("../timeline/")
from cronjob.jobs import run_jobs

if __name__ == '__main__':
    run_jobs()
