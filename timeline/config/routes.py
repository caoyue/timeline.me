#-*- coding: utf-8 -*-

import config

VIEW = 'view.'

# routes
urls = (
    '/', VIEW + 'home.index',
    '/index/(\d+)', VIEW + 'home.index',
    '/(%s)' % config.source_filter, VIEW + 'home.source',
    '/(%s)/' % config.source_filter, VIEW + 'home.source',
    '/(%s)/(\d+)' % config.source_filter, VIEW + 'home.source',
    '/feed', VIEW + "home.feed",
    '/weibo/signin', VIEW + 'weibo.signin',
    '/weibo/callback', VIEW + 'weibo.callback',
    '/weibo/test', VIEW + 'weibo.test',
    '/twitter/signin', VIEW + 'twitter.signin',
    '/twitter/callback', VIEW + 'twitter.callback',
    '/cron', VIEW + 'cron.index',
    '/cron/(timeline|statistic)', VIEW + 'cron.index',
    '/login', VIEW + 'login.index',
    '/update', VIEW + 'update.index',
    '/past', VIEW + 'past.index',
    '/past/([0-9]{4}-[0-9]{2}-[0-9]{2})', VIEW + 'past.index',
    '/statistic', VIEW + 'statistic.index',
    '/statistic/([0-9]{4})', VIEW + 'statistic.index',
    '/search', VIEW + 'ssearch.index',
    '/search/([^\/]+)', VIEW + 'ssearch.index',
    '/search/([^\/]+)/(\d+)', VIEW + 'ssearch.index'
)
