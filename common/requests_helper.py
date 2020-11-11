#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：ApiTest -> requests_helper.py
@IDE    ：PyCharm
@Author ：ArthurWxy
@Date   ：2020/11/11 2:33 PM
@Desc   ：
=================================================="""
import json
import traceback
import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class ShareAPI(object):
    def __init__(self):
        self.s = requests.Session()
        self.login_url = 'https://ones.ai/project/api/project/auth/login'
        self.header = {
            "user-agent": "user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/78.0.3904.108 Safari/537.36",
            "content-type": "application/json"}

    def login(self, login_credential):
        try:
            result = self.s.post(self.login_url, data=json.dumps(login_credential), headers=self.header, verify=False)
            if int(result.status_code) == 200:
                pass
            else:
                raise Exception('login failed')
            return result
        except RuntimeError:
            traceback.print_exc()

    def post_api(self, url, **kwargs):
        return self.s.post(url, **kwargs)

    def get_api(self, url, **kwargs):
        return self.s.get(url, **kwargs)