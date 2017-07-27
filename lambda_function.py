# coding:utf-8

import os
import logging
import logging.config
import traceback
from ec2 import Ec2
from slack import Slack


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    slack = Slack()
    try:

        target_name = os.environ['TARGET_NAME']

        ec2 = Ec2()

        instance_ids = ec2.get_instance_id_by_name(target_name)
        if len(instance_ids) == 0:
            message = u'{target_name} : instance is None'.format(
                target_name=target_name
            )
            logger.info(message)
            slack.sendMessage(message, "#ec2_create_image")
            return

        response = ec2.create_images(instance_ids, target_name)
        ec2.create_tag_for_image(response, target_name)
        logger.info(response)
        slack.sendMessage(
            '{target_name}\n{response}'.format(
                target_name=target_name,
                response=response
            ),
            "#ec2_create_image"
        )

        image_infos = ec2.get_image_info_by_tag(
            target_name,
            purge_days=int(os.environ.get('PURGE_DAYS', '7')),
            owners=os.environ['AWS_ACCOUNT_ID']
        )

        response = ec2.deregister_images(image_infos)
        if len(response) > 0:
            for res in response:
                slack.sendMessage(
                    '{target_name}\n{response} is deregisted'.format(
                        target_name=target_name,
                        response=res
                    ),
                    "#ec2_create_image"
                )

        response = ec2.delete_snapshot(image_infos)
        if len(response) > 0:
            for res in response:
                slack.sendMessage(
                    '{target_name}\n{response} is deleted'.format(
                        target_name=target_name,
                        response=res
                    ),
                    "#ec2_create_image"
                )


    except Exception as e:
        slack.sendMessage('ec2_create_image:' + traceback.format_exc(), "#ec2_create_image")
        logger.error(traceback.format_exc())
        raise Exception(traceback.format_exc())

