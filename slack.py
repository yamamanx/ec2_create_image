# -*- coding: utf-8 -*-

import requests
import json
import os

class Slack(object):

    def __init__(self):
        self.url = os.environ['SLACK_URL']

    def sendMessage(self,content,channel):
        payload_dic = {
            "text": content,
            "channel": channel,
        }
        requests.post(self.url, data=json.dumps(payload_dic))