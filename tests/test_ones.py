#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：ApiTest -> test_ones.py
@IDE    ：PyCharm
@Author ：ArthurWxy
@Date   ：2020/11/11 1:21 PM
@Desc   ：
=================================================="""
import json
import requests
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.ones import OneAI


class TestOneAI:

    @pytest.mark.parametrize('login_data, project_name, target_page',
                             [({"password": "wxy1996.com", "email": "kzzn@qq.com"},
                            {"project_name": "VIPTEST"}, {"target_page": "https://ones.ai/project/#/home/project"})])
    def test_project_name_txt(self, login_data, project_name, target_page):
        print(login_data)
        one_page = OneAI(login_data, target_page)
        actual_project_name = one_page.get_project_name()
        assert actual_project_name == project_name["project_name"]


def cookie_to_selenium_format(cookie):
    cookies_selenium_mapping = {'path': '',
                                'secure': '',
                                'name': '',
                                'value': '',
                                'expires': ''
                                }
    cookie_dict = {}

    if getattr(cookie, 'domain_initial_dot'):
        cookie_dict['domain'] = '.' + getattr(cookie, 'domain')
    else:
        cookie_dict['domain'] = getattr(cookie, 'domain')

    for k in list(cookies_selenium_mapping.keys()):
        key = k
        value = getattr(cookie, k)
        cookie_dict[key] = value

    return cookie_dict


class TestOneAI:

    def setup_method(self, method):
        self.s = requests.Session()
        self.login_url = 'https://ones.ai/project/api/project/auth/login'
        self.home_page = 'https://ones.ai/project/#/home/project'
        self.header = {
            "user-agent": "user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/78.0.3904.108 Safari/537.36",
            "content-type": "application/json"}
        self.driver = webdriver.Chrome()

    @pytest.mark.parametrize('login_data, project_name', [({"password": "wxy1996.com",
                                                            "email": "kzzn@qq.com"},
                                                           {"project_name": "wxy1996.com"})])
    def test_merge_api_ui(self, login_data, project_name):
        result = self.s.post(self.login_url, data=json.dumps(login_data), headers=self.header)
        assert result.status_code == 200
        assert json.loads(result.text)["user"]["email"].lower() == login_data["email"]
        all_cookies = self.s.cookies._cookies[".ones.ai"]["/"]
        self.driver.get(self.home_page)
        self.driver.delete_all_cookies()
        for k, v in all_cookies.items():
            print(v)
            print(type(v))
            self.driver.add_cookie(cookie_to_selenium_format(v))
        self.driver.get(self.home_page)
        try:
            element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[class="company-title-text"]')))
            assert element.get_attribute("innerHTML") == project_name["project_name"]
        except TimeoutError:
            raise TimeoutError('Run time out')

    def teardown_method(self, method):
        self.s.close()
        self.driver.quit()