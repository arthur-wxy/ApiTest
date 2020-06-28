#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：ApiTest -> compare.py
@IDE    ：PyCharm
@Author ：ArthurWxy
@Date   ：2020/6/28 4:28 PM
@Desc   ：
=================================================="""
import os
import json
import logging

from common import opmysql
from public import config

operation_db = opmysql.OperationDbInterface()


class CompareParam(object):
    # 初始化数据
    def __init__(self, params_interface):
        """
        关键字code的比较
        :param params_interface: 接口入参
        """
        self.params_interface = params_interface
        self.id_case = params_interface['id']
        self.result_list_response = []  # 定义存参数集的空列表
        self.params_to_compare = params_interface['params_to_compare']  # 定义参数完整性的预期结果

    def compare_code(self, result_interface):
        """
        :param result_interface: http返回包数据
        :return: 返回码code，返回信息message，数据data
        """
        try:
            if result_interface.startswith('{') and isinstance(result_interface, str):
                temp_result_interface = json.loads(result_interface)  # 转换为字典类型
                temp_code_to_compare = self.params_interface['code_to_compare']  # 获取待比较的code
                if temp_code_to_compare in temp_result_interface.keys():
                    if str(temp_result_interface[temp_code_to_compare]) == str(self.params_interface['code_expect']):
                        result = {'code': '0000', 'message': '关键字参数值相同', 'data': []}
                        operation_db.op_sql("update case_interface set code_actual='%s',"
                                            "code_compare_result=%s where id=%s"
                                            %(temp_result_interface[temp_code_to_compare], 1, self.id_case))
                    elif str(temp_result_interface[temp_code_to_compare]) != str(self.params_interface['code_expect']):
                        result = {'code': '1003', 'message': '关键字参数值不相同', 'data': []}
                        operation_db.op_sql("update case_interface set code_actual='%s',"
                                            "code_compare_result=%s where id=%s"
                                            %(temp_result_interface[temp_code_to_compare], 0, self.id_case))
                    else:
                        result = {'code': '1002', 'message': '关键字参数值比较出错', 'data': []}
                        operation_db.op_sql("update case_interface set code_actual='%s',"
                                            "code_compare_result=%s where id=%s"
                                            % (temp_result_interface[temp_code_to_compare], 3, self.id_case))

