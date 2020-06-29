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
                                            % (temp_result_interface[temp_code_to_compare], 1, self.id_case))
                    elif str(temp_result_interface[temp_code_to_compare]) != str(self.params_interface['code_expect']):
                        result = {'code': '1003', 'message': '关键字参数值不相同', 'data': []}
                        operation_db.op_sql("update case_interface set code_actual='%s',"
                                            "code_compare_result=%s where id=%s"
                                            % (temp_result_interface[temp_code_to_compare], 0, self.id_case))
                    else:
                        result = {'code': '1002', 'message': '关键字参数值比较出错', 'data': []}
                        operation_db.op_sql("update case_interface set code_actual='%s',"
                                            "code_compare_result=%s where id=%s"
                                            % (temp_result_interface[temp_code_to_compare], 3, self.id_case))
                else:
                    result = {'code': '1001', 'message': '返回包数据无关键字参数', 'data': []}
                    operation_db.op_sql("update case_interface set code_actual='%s',"
                                        "code_compare_result=%s where id=%s"
                                        % (2, self.id_case))
            else:
                result = {'code': '1000', 'message': '返回包格式不合法', 'data': []}
                operation_db.op_sql("update case_interface set code_actual='%s',"
                                    "code_compare_result=%s where id=%s"
                                    % (4, self.id_case))
        except Exception as error:
            result = {'code': '9999', 'message': '关键值参数值比较异常', 'data': []}
            operation_db.op_sql("update case_interface set code_actual='%s',"
                                "code_compare_result=%s where id=%s"
                                % (9, self.id_case))
            logging.basicConfig(
                filename=config.src_path + '/Users/arthurw/PycharmProjects/ApiTest/log/syserror.log',
                level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line: %(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
        finally:
            return result

    # 接口返回数据中的参数名写入列表
    def get_compare_params(self, result_interface):
        """
        :param result_interface: http返回包数据
        :return: 返回码code，返回信息message，数据data
        """
        try:
            if result_interface.startswith('{') and isinstance(result_interface, str):
                temp_result_interface = json.loads(result_interface)  # 转换为字典类型
                self.result_list_response = temp_result_interface.keys()
                result = {'code': '0000', 'message': '成功', 'data': []}
            else:
                result = {'code': '1000', 'message': '返回包格式不合法', 'data': []}
        except Exception as error:
            result = {'code': '9999', 'message': '处理数据异常', 'data': []}
            logging.basicConfig(
                filename=config.src_path + '/Users/arthurw/PycharmProjects/ApiTest/log/syserror.log',
                level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line: %(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
        finally:
            return result

    # 递归方法
    def __recur_params(self, result_interface):
        # 定义递归操作，将接口返回数据中的参数名写入列表中（去重）
        try:
            if result_interface.startswith('{') and isinstance(result_interface, str):
                temp_result_interface = json.loads(result_interface)
                self.__recur_params(temp_result_interface)
            elif isinstance(result_interface, dict):  # 如果入参是字典
                for param, value in result_interface.items():
                    self.result_list_response.append(param)
                    if isinstance(value, list):
                        for param in value:
                            self.__recur_params(param)
                    elif isinstance(value, dict):
                        self.__recur_params(value)
                    else:
                        continue
            else:
                pass
        except Exception as error:
            logging.basicConfig(
                filename=config.src_path + '/Users/arthurw/PycharmProjects/ApiTest/log/syserror.log',
                level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line: %(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
            return {'code': '9999', 'message': '处理数据异常', 'data': []}
        return {'code': '0000', 'message': '成功', 'data': list(set(self.result_list_response))}

    # 定义参数完整性的比较方法，将传参与__recur_params方法返回结果进行比较
    def compare_params_complete(self, result_interface):
        """
        :param result_interface: http返回包数据
        :return: 返回码code，返回信息message，数据data
        """
        try:
            temp_compare_params = self.__recur_params(result_interface)  # 获取返回包的参数集
            if temp_compare_params['code'] == '0000':
                temp_result_list_response = temp_compare_params['data']  # 获取接口返回参数去重列表
                # 判断预期结果集是否为列表
                if self.params_to_compare.startswith('[') and isinstance(self.params_to_compare, str):
                    list_params_to_compare = eval(self.params_to_compare)  # 将数据库中的unicode转换成原列表
                    if set(list_params_to_compare).issubset(set(temp_result_list_response)):  # 判断集合的包含关系
                        result = {'code': '0000', 'message': '参数完整性一致', 'data': []}
                        operation_db.op_sql("update case_interface set params_actual='%s',"
                                            "params_compare_result=%s where id=%s"
                                            % (temp_result_list_response, 1, self.id_case))
                    else:
                        pass
