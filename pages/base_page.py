#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：ApiTest -> base_page.py
@IDE    ：PyCharm
@Author ：ArthurWxy
@Date   ：2020/11/11 1:22 PM
@Desc   ：
=================================================="""
import json
import requests

from selenium import webdriver
from page_objects import PageObject, PageElement
from common.selenium_helper import SeleniumHelper
from common.requests_helper import ShareAPI


def cookie_to_selenium_format(cookie):
    cookie_selenium_mapping = {'path': '', 'secure': '', 'name': '', 'value': '', 'expires': ''}
    cookie_dict = {}
    if getattr(cookie, 'domain_initial_dot'):
        cookie_dict['domain'] = '.' + getattr(cookie, 'domain')
    else:
        cookie_dict['domain'] = getattr(cookie, 'domain')
    for k in list(cookie_selenium_mapping.keys()):
        key = k
        value = getattr(cookie, k)
        cookie_dict[key] = value
    return cookie_dict


class BasePage(PageObject):

    def __init__(self, login_credential, target_page):
        self.api_driver = ShareAPI()
        self.loginResult = self.api_driver.login(login_credential)
        self.driver = SeleniumHelper.initial_driver()
        self._api_login(login_credential, target_page)

    def _api_login(self, login_credential, target_page):
        target_url = json.loads(json.dumps(target_page))
        assert json.loads(self.loginResult.text)["user"]["email"].lower() == login_credential["email"]

        all_cookies = self.loginResult.cookies._cookies[".ones.ai"]["/"]
        self.driver.get(target_url["target_page"])
        self.driver.delete_all_cookies()
        for k, v in all_cookies.items():
            self.driver.add_cookie(SeleniumHelper.cookie_to_selenium_format(v))
        self.driver.get(target_url["target_page"])
        return self.driver
