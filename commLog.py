#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2015 Sengled, Inc.
# All Rights Reserved.

# @author: WShuai, Sengled, Inc.

import logging
from logging.handlers import RotatingFileHandler

'''
LOG
'''
class CommonLog(object):
    def __init__(self, logfile, level):
        self.log_level = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARN': logging.WARNING,
            'ERROR': logging.ERROR,
        }
        self.filename = logfile
        self.level = self.log_level[level.upper()]
        self.format = logging.Formatter('[%(asctime)s] [%(process)d] [%(thread)d] [%(filename)20s] [line:%(lineno)4d] [%(levelname)-6s] %(message)s')
        self.logger = None
        return

    def register(self):
        handler = RotatingFileHandler(self.filename, maxBytes = 200*1024*1024, backupCount = 20)
        handler.setFormatter(self.format)
        self.logger = logging.getLogger(self.filename)
        self.logger.addHandler(handler)
        self.logger.setLevel(self.level)
        return self.logger

def get_logger(logfile, level):
    common_log = CommonLog(logfile, level)
    return common_log.register()

'''
例子
'''

import sys
import time
if __name__ == '__main__':
    # init log
    log_file = './test.log'
    log_level = 'DEBUG'
    LOG = get_logger(log_file, log_level)

    while True:
        LOG.debug('this is debug log')
        LOG.info('this is info log')
        LOG.error('this is error log')
        time.sleep(0.01)
    sys.exit(0)
