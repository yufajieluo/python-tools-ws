#!/usr/bin/python
# -*- coding:utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2016 WShuai, Inc.
# All Rights Reserved.

# @author: WShuai, WShuai, Inc.

'''
Get New Version
'v{0}.{1}.{2}'.format(major_version.minor_version.revise_version)
major_version - 
minor_version - max is 9, greater will by carry to major_version
revise_version - max is 99, greater will by carry to minor_version
'''

class VersionHandler(object):
    def __init__(self, last_version):
        self.last_version = last_version
        return

    def get_new_version(self):
        if not self.last_version:
            new_version = 'v1.0.0'
        else:
            major_version = int(self.last_version[1:].split('.')[0])
            minor_version = int(self.last_version[1:].split('.')[1])
            revise_version = int(self.last_version[1:].split('.')[2])
            print('major_version is [{0}], minor_version is [{1}], revise_version is [{2}]'.format(major_version, minor_version, revise_version))
            if revise_version < 99:
                revise_version += 1
            else:
                revise_version = 0
                minor_version += 1

            print('major_version is [{0}], minor_version is [{1}], revise_version is [{2}]'.format(major_version, minor_version, revise_version))
            if minor_version >= 10:
                minor_version = 0
                major_version += 1
            new_version = 'v{0}.{1}.{2}'.format(major_version, minor_version, revise_version)
        return new_version

import sys
if __name__ == '__main__':
    if len(sys.argv) != 2:
        last_version = None
    else:
        last_version = sys.argv[1]

    version_handler = VersionHandler(last_version)
    print version_handler.get_new_version()
