#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2015 Sengled, Inc.
# All Rights Reserved.

# @author: WShuai, Sengled, Inc.

import time

class TimerProcess(object):
    def __init__(self):
        self.timers = []
        return
    def add_timer(self, timer):
        if timer in self.timers:
            return
        self.timers.append(timer)

    def del_timer(self, timer):
        if timer in self.timers:
            self.timers.remove(timer)
        return

    def start_timer(self):
        for timer in self.timers:
            timer.start_timer()
    def deamon_loop(self):
        self.start_timer()
        while True:
            for timer in self.timers:
                try:
                    timer.count_timer()
                except Exception as e:
                    print ('unknown error(%s) when process timer %s' % (e,timer.process))
                    continue
            time.sleep(1)
        return

class Timer(object):
    def __init__(self, interval, process, parameters = None, delay_second = 0):
        self.interval = interval
        self.process = process
        self.parameters = parameters
        self.tmp = delay_second
        self.start = 0
        return

    def start_timer(self):
        self.start = time.time()
        return

    def count_timer(self):
        now = time.time()
        elapse = now - self.start
        self.start = now
        if elapse > 0:
            self.tmp -= elapse
            if self.tmp < 0:
                return self.run()
        if time.time() - self.start >= self.interval:
            return self.start_timer()

    def run(self):
        self.tmp = self.interval
        return self.process(self.parameters)

        
'''
例子
'''

import sys

def test_func(parameters = None):
    print 'parameters is {0}, now time is {1}'.format(parameters, time.strftime('%Y-%m-%d %H:%M:%S'))
    return
    

if __name__ == '__main__':
    # -- init timer ---
    timer_process = TimerProcess()
    # -- init end   ---
    
    test_timer = Timer(10, test_func, delay_second = 5, parameters = {'name': 'wshuai', 'sex': 'male'})
    timer_process.add_timer(test_timer)
    
    print('this thread is begin.')
    timer_process.deamon_loop()
    print('this thread is exit.')
    sys.exit(0)
