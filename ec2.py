# coding:utf-8


import boto3
import logging
import os
import util


logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Ec2(object):

    def __init__(self):

        self.region_name = os.environ['REGION_NAME']
        self.client = boto3.client('ec2', self.region_name)
        self.resource = boto3.resource('ec2', self.region_name)

    def create_images(self, instance_ids, target_name):
        response = []
        for id in instance_ids:
            instance = self.resource.Instance(id)
            image_name = '{name}_{date}'.format(
                name=target_name,
                date=util.today_str()
            )
            response.append(instance.create_image(
                Name=image_name))
        return response

    def create_tag_for_image(self, images, target_name):
        for image in images:
            image.create_tags(
                Tags=[
                    {
                        'Key': 'AutoCreateFor',
                        'Value': target_name
                    }
                ]
            )

    def delete_snapshot(self, image_infos):
        response = []
        for info in image_infos:
            for device in info['devices']:
                snap_shot = self.resource.Snapshot(
                    device['Ebs']['SnapshotId'])
                snap_shot.delete()
                response.append(device['Ebs']['SnapshotId'])
        return response

    def deregister_images(self, image_infos):
        response = []
        for info in image_infos:
            image = self.resource.Image(info['image_id'])
            image.deregister()
            response.append(info['image_id'])
        return response

    def get_image_info_by_name(self, target_name, purge_days=7, owners=None):
        targets = []
        response = self.client.describe_images(
            Owners=[owners]
        )
        for image in response['Images']:
            if image['Name'][0:len(target_name)] == target_name:
                create_date = util.datetime_from_str(
                    image['CreationDate'])
                if util.now_time() >= util.after_day(
                        create_date, purge_days):
                    targets.append(
                        {
                            'image_id': image['ImageId'],
                            'devices': image['BlockDeviceMappings']
                        }
                    )
        return targets

    def get_image_info_by_tag(self, target_name, purge_days=7, owners=None):
        targets = []
        response = self.client.describe_images(
            Owners=[owners]
        )
        for image in response['Images']:
            for tag in image.tags:
                if tag['Key'] == 'AutoCreateFor':
                    if tag['Value'] == target_name:
                        create_date = util.datetime_from_str(
                            image['CreationDate'])
                        if util.now_time() >= util.after_day(
                                create_date, purge_days):
                            targets.append(
                                {
                                    'image_id': image['ImageId'],
                                    'devices': image['BlockDeviceMappings']
                                }
                            )
        return targets

    def get_instance_id_by_name(self, target_name):
        targets = []
        response = self.client.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if 'Tags' in instance:
                    for tag in instance['Tags']:
                        if tag['Key'] == 'Name':
                            if tag['Value'] == target_name:
                                targets.append(instance['InstanceId'])
        return targets

    def start_instances(self, instance_ids):
        response = self.client.start_instances(InstanceIds=instance_ids)
        return response

    def stop_instances(self, instance_ids):
        response = self.client.stop_instances(InstanceIds=instance_ids)
        return response




