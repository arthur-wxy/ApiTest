# _*_ coding:utf-8 _*_

import xlrd


class ReadExcel():
    """ 读取excel文件数据"""
    def __init__(self, file_name, sheet_name="Sheet1"):
        self.data = xlrd.open_workbook(file_name)
        self.table = self.data.sheet_by_name(sheet_name)
        # 获取总行数量