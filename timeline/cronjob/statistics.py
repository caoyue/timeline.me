#-*- coding: utf-8 -*-

from model.statistic import StatisticData as s
from utils.mytime import get_time as now


def statistics():
    print ">> [%s]Start statistic..." % now()

    for t in ['hour', 'month', 'source']:
        for y in [None, now().year]:
            s.set_statistic(t, y)

    print ">> [%s]End statistic." % now()
    print "---------------"
