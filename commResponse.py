#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2016 Wshuai, Inc.
# All Rights Reserved.

# @author: WShuai, Wshuai, Inc.

'''
Generate response message, such as: 
{
    "rsp_head": {
        "rsp_code": 200,
        "rsp_info": "success"
    }
}

or

{
    "rsp_head": {
        "rsp_code": 200,
        "rsp_info": "success"
    },
    "rsp_body": {
        "games": [
            {
                "name": "WOW",
                "type": "MMO"
            },
            {
                "name": "SC",
                "type": "RTS"
            },
            {
                "name": "wow",
                "type": "RPG"
            }
        ]
    }
}
'''
class CommResponse(object):
    def __init__(self):
        self.rsp_info = {
            # system
            200: 'success',
            29001: 'parameter error',
            29999: 'system error',
        }

    def generate_rsp_msg(self, rsp_code, rsp_body):
        try:
            rsp_info = self.rsp_info[rsp_code]
        except:
            rsp_info = 'failed'
        rsp_head = {
            'rsp_head': {
                'rsp_code': rsp_code,
                'rsp_info': rsp_info,
            }
        }
        if not rsp_body:
            return rsp_head
        else:
            return dict(rsp_head.items() + rsp_body.items())
