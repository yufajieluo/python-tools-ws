#!/usr/bin/python
# -*- coding:utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2016 Wshuai, Inc.
# All Rights Reserved.

# @author: WShuai, Wshuai, Inc.

import os
import re
import sys
import time
import statvfs

'''
Clear LOG
'''
class Scavenger(object):
    '''
    mnt_path - str: 要清理的本地挂载路径, 例如: /var/log
    threshold - int: 触发清理的阈值, 当小于 {threshold}% 阈值时, 触发清理动作
    default_files - list: 没有做轮转的文件, 采用 echo '' > {file} 的方式清空
    '''
    def __init__(self, mnt_path, threshold, default_files):
        self.mnt_path = mnt_path
        self.threshold = threshold
        self.default_files = default_files
        return

    def trigger(self):
        vfs = os.statvfs(self.mnt_path)
        if float(vfs[statvfs.F_BAVAIL]) / vfs[statvfs.F_BLOCKS] * 100 < self.threshold:
            trigger = True
        else:
            trigger = False
        return trigger

    def clear(self, log_path):
        '''
        log_path - str: 要清理的本地路径
        '''
        now_date = time.strftime('%Y-%m-%d', time.localtime())
        result = os.walk(log_path)
        for path, dirs, files in result:
            for file in files:
                if file[-3:] == '.gz' or file[-4:] == '.zip': # such as xxx.tar.gz and xxx.zip
                    print 'remove [%s]' % os.path.join(path, file)
                    self.remove_file(os.path.join(path, file))
                if re.search(r'\d{4}-\d{2}-\d{2}', file): # such as xxx.2017-03-29.xxx
                    print 'remove [%s]' % os.path.join(path, file)
                    self.remove_file(os.path.join(path, file))
                if re.search(r'.log.\d{1}', file): # such as xxx.log.1
                    print 'remove [%s]' % os.path.join(path, file)
                    self.remove_file(os.path.join(path, file))
                '''
                such as xxx.INFO -> xxx.log.INFO.20170328-053335.31241
                remove log file exclude current day's.
                '''
                if file[:23] == 'media_process_server.ip':
                    file_date = file.split('.')[5].split('-')[0]
                    file_format_date = '%s-%s-%s' % (file_date[:4], file_date[4:6], file_date[-2:])
                    if file_format_date < now_date:
                        print 'remove [%s]' % os.path.join(path, file)
                        self.remove_file(os.path.join(path, file))
                for default_file in self.default_files:
                    if file == default_file:
                        print 'clear [%s]' % os.path.join(path, file)
                        self.clear_file(os.path.join(path, file))

    def remove_file(self, file):
        try:
            os.remove(file)
            print 'remove file [%s] success' % file
        except Exception as e:
            print 'remove file [%s] failed' % file
        return
    
    def clear_file(self, file):
        try:
            os.system("echo '' > {0}".format(file))
            print 'clear file [%s] success' % file
        except Exception as e:
            print 'clear file [%s] failed' % file
        return


'''
使用例子
'''
if __name__ == '__main__':
    mnt_path = '/var/log'
    threshold = 30
    default_files = ['catalina_out.log']
    log_paths = ['/var/log/sengled']

    scavenger = Scavenger(mnt_path, threshold, default_files)
    if not scavenger.trigger():
        print 'disk space is enougth, I will to my rest. ~\(^.^)/~'
        sys.exit(0)

    print 'disk space is not enougth, I am going to work. ~\(>.<)/~'

    for log_path in log_paths:
        scavenger.clear(log_path)
        print '================'

    sys.exit(0)
