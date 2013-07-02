#-*- coding: utf-8 -*-

import config

CONTROLLER = 'view.'

# routes
urls = (
    '/', CONTROLLER + 'home.index',
    '/(\d+)', CONTROLLER + 'home.index',
    '/(%s)' % config.source_filter, CONTROLLER + 'home.source',
    '/(%s)/' % config.source_filter, CONTROLLER + 'home.source',
    '/(%s)/(\d+)' % config.source_filter, CONTROLLER + 'home.source',
    '/feed', CONTROLLER + "home.feed",
    '/weibo/signin', CONTROLLER + 'weibo.signin',
    '/weibo/callback', CONTROLLER + 'weibo.callback',
    '/weibo/test', CONTROLLER + 'weibo.test',
    '/twitter/signin', CONTROLLER + 'twitter.signin',
    '/twitter/callback', CONTROLLER + 'twitter.callback',
    '/cronjob', CONTROLLER + 'cron.jobs',
    '/login', CONTROLLER + 'login.index',
    '/update', CONTROLLER + 'update.index'
)
