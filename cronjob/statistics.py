#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
sys.path.append("../timeline/")

from cronjob.statistics import statistics

if __name__ == '__main__':
    statistics()
