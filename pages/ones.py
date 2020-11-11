#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：ApiTest -> ones.py
@IDE    ：PyCharm
@Author ：ArthurWxy
@Date   ：2020/11/11 1:22 PM
@Desc   ：
=================================================="""
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page_objects import PageObject, PageElement
from pages.base_page import BasePage


class OneAI(BasePage):
    PROJECT_NAME_LOCATOR = '[class="company-title-text"]'
    NEW_PROJECT_LOCATOR = '.ones-btn.ones-btn-primary'
    new_project = PageElement(css=NEW_PROJECT_LOCATOR)

    def __init__(self, login_credential, target_page):
        super().__init__(login_credential, target_page)

    def get_project_name(self):
        try:
            project_name = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.PROJECT_NAME_LOCATOR)))
            return project_name.get_attribute("innerHTML")
        except TimeoutError:
            raise TimeoutError('Run time out')


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


class OneAI(PageObject):
    # 使用page_objects库把元素locator， 元素定位，元素操作分离
    # 元素定位的字符串
    PROJECT_NAME_LOCATOR = '[class="company-title-text"]'
    NEW_PROJECT_LOCATOR = '.ones-btn.ones-btn-primary'
    # 元素定位
    new_project = PageElement(css=NEW_PROJECT_LOCATOR)

    # 通过构造函数初始化浏览器driver，requests.Session()
    # 通过api_login方法直接带登录态到达待测试页面开始测试
    def __init__(self, login_credential, target_page):
        self.login_url = 'https://ones.ai/project/api/project/auth/login'
        self.header = {
            "user-agent": "user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/78.0.3904.108 Safari/537.36",
            "content-type": "application/json"}
        self.s = requests.Session()
        self.driver = webdriver.Chrome()
        self.api_login(login_credential, target_page)

    # 融合API测试和UI测试，并传递登录态到浏览器Driver供使用
    def api_login(self, login_credential, target_page):
        target_url = json.loads(json.dumps(target_page))
        try:
            result = self.s.post(self.login_url, data=json.dumps(login_credential), headers=self.header)
            assert result.status_code == 200
            assert json.loads(result.text)["user"]["email"].lower() == login_credential["email"]
        except Exception:
            raise Exception("Login Failed, please check!")
        all_cookies = self.s.cookies._cookies[".ones.ai"]["/"]
        self.driver.get(target_url["target_page"])
        self.driver.delete_all_cookies()
        for k, v in all_cookies.items():
            self.driver.add_cookie(cookie_to_selenium_format(v))
        self.driver.get(target_url["target_page"])
        return self.driver

    # 功能函数
    def get_project_name(self):
        try:
            project_name = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.PROJECT_NAME_LOCATOR)))
            return project_name.get_attribute("innerHTML")
        except TimeoutError:
            raise TimeoutError('Run time out')