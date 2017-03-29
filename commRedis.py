#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2015 Sengled, Inc.
# All Rights Reserved.

# @author: WShuai, Sengled, Inc.

'''
Redis Connection
pip install redis
'''

import redis

class RedisHandler(object):
    def __init__(self, redis_addr, redis_port, redis_pwd, redis_db):
        self.redis_addr = redis_addr
        self.redis_port = redis_port
        self.redis_pwd  = redis_pwd
        self.redis_db = redis_db
        self.redis_conn = None
    def connect(self):
        try:
            self.redis_conn = redis.Redis(host = self.redis_addr, port = self.redis_port, password = self.redis_pwd, db = self.redis_db)
            self.redis_conn.ping()
            print 'connect to redis successful.'
            return True
        except Exception as e:
            print('connect to redis failed: {0}'.format(e))
            return False

'''
例子
'''
import sys
if __name__ == '__main__':
    redis_handler = RedisHandler('127.0.0.1', 6379, None, 1)
    if not redis_handler.connect():
        print('conntect redis failed')
        sys.exit(1)
    print redis_handler.redis_conn.hgetall('peple')
    sys.exit(0)
