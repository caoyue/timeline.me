#-*- coding:utf-8 -*-

import logging
from config import config


logging.basicConfig(
    format='%(asctime)s %(name)-12s %(levelname)-12s %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
    filename=config.LOG_PATH_NAME)
