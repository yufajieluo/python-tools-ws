#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2017 Wshuai, Inc.
# All Rights Reserved.

# @author: WShuai, Wshuai, Inc.

import os
import requests

'''
Http Client
pip install requests
'''
class HttpClient(object):
    '''
    host - str: 主机地址, 如: 127.0.0.1 或 www.baidu.com
    port - str or int: 主机端口 
    '''
    def __init__(self, host, port):
        self.host = host
        self.port = port
        return

    def post(self, url, json_body):
        '''
        url - str: URL资源路径
        json_body - json object: 参数 
        '''
        request_url = 'http://{0}:{1}/{2}'.format(self.host, self.port, url)
        try:
            result = requests.post(request_url, data = json_body, timeout = 15)
            print result.status_code
            if result.status_code != 200:
                data = False
            else:
                data = result.text
        except Exception as e:
            data = False
        return data

    def get(self, url, json_body, ssl = None):
        '''
        url - str: URL资源路径
        json_body - json object: 参数 
        '''
        if url[0] == '/':
            url = url[1:]

        if not ssl:
            request_url = 'http://{0}:{1}/{2}'.format(self.host, self.port, url)
        else:
            request_url = 'https://{0}:{1}/{2}'.format(self.host, self.port, url)
        try:
            result = requests.get(request_url, params = json_body, timeout = 15)
            if result.status_code != 200:
                data = False
            else:
                data = result.text
        except Exception as e:
            data = False
        return data

'''
例子
'''
import sys
if __name__ == '__main__':
    http_client = HttpClient('169.254.169.254', 80)
    print http_client.get('/latest/meta-data/instance-id', {})
    sys.exit(0)
