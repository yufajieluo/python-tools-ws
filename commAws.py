#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2017 Sengled, Inc.
# All Rights Reserved.

# @author: WShuai, Sengled, Inc.

import boto3

'''
AWS api
pip install boto3
'''

class EC2Handler(object):
    def __init__(self, region_name, aws_access_key_id, aws_secret_access_key):
        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        return

    def connect(self):
        self.client = boto3.client(
            'ec2',
            region_name = self.region_name,
            aws_access_key_id = self.aws_access_key_id,
            aws_secret_access_key = self.aws_secret_access_key
        )
        return

    def get_tags(self, instance_id, tag_key):
        response = self.client.describe_tags(
            DryRun = False,
            Filters = [
                {
                    'Name': 'resource-type',
                    'Values': ['instance']
                },
                {
                    'Name': 'resource-id',
                    'Values': [instance_id]
                },
                {
                    'Name': 'key',
                    'Values': [tag_key]
                }
            ]
        )
        return response['Tags']

class AsgHandler(object):
    def __init__(self, region_name, aws_access_key_id, aws_secret_access_key):
        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        return

    def connect(self):
        self.client = boto3.client(
            'autoscaling',
            region_name = self.region_name,
            aws_access_key_id = self.aws_access_key_id,
            aws_secret_access_key = self.aws_secret_access_key
        )
        return

    def get_asg_info(self, group_name):
        response = self.client.describe_auto_scaling_groups(
            AutoScalingGroupNames = [group_name]
        )
        return response['AutoScalingGroups']

    def detach_instances(self, asg_name, instance_ids):
        response = self.client.detach_instances(
            AutoScalingGroupName = asg_name,
            InstanceIds = instance_ids,
            ShouldDecrementDesiredCapacity = False
        )
        return

class S3Handler(object):
    def __init__(self, region_name, access_key_id, secret_access_key):
        self.region_name = region_name
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.bucket_name = None
        self.bucket = None
        self.conn = None
        self.region = None
        return

    def connect(self):
        if self.conn:
            return
        try:
            self.conn = boto3.resource(
                's3',
                region_name = self.region_name,
                aws_access_key_id = self.access_key_id,
                aws_secret_access_key = self.secret_access_key
            )
        except Exception as e:
            print('connect to aws s3 failed, {0}'.format(e))
        return

    def get_file(self, bucket_name, remote_path_file, local_path_file):
        self.bucket = self.conn.Bucket(bucket_name)
        self.bucket.download_file(remote_path_file, local_path_file)
        return

    def put_file(self, bucket_name, remote_path_file, local_path_file):
        self.bucket = self.conn.Bucket(bucket_name)
        self.bucket.upload_file(local_path_file, remote_path_file)
        return
