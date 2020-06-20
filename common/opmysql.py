# -*- coding:utf-8 -*-
import os
import logging
import pymysql

from public import config


class OperationDbInterface(object):
    # 初始化连接
    """
        :param host_db:数据库主机
        :param user_db:用户名
        :param password_db:密码
        :param name_db:数据库名
        :param port_db:端口号
        :param link_type:连接类型，用于设置输出数据是元组还是字典，默认字典0
        :return:游标
        """

    def __init__(self, host_db='10.2.12.132', user_db='root', password_db='123456',
                 name_db='test_interface', port_db='3306', link_type=0):

        try:
            if link_type == 0:
                # 创建数据库连接，返回字典
                self.conn = pymysql.connect(host=host_db, user=user_db, passwd=password_db, db=name_db,
                                            port=port_db, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
            else:
                self.conn = pymysql.connect(host=host_db, user=user_db, passwd=password_db, db=name_db,
                                            port=port_db, charset='utf8')  # 返回元组
                self.cur = self.conn.cursor()
        except pymysql.Error as e:
            print('创建数据库连接失败|Mysql Error %d: %s' % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + 'C:\\Users\\user\\Desktop\\test_interface\\syserror.log',
                                levell=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line: %(lineo)d]%(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)

    def op_sql(self, condition):
        """
        :param condition: sql语句
        :return: 字典形式
        """
        try:
            self.cur.execute(condition)  # 执行sql语句
            self.conn.commit()  # 提交游标数据
            result = {'code': '0000', 'message': '执行操作成功', 'data': []}
        except pymysql.Error as e:
            result = {'code': '9999', 'message': '执行操作异常', 'data': []}
            print('数据库错误|op_sql %d: %s' % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + 'C:\\Users\\user\\Desktop\\test_interface\\syserror.log',
                                levell=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line: %(lineo)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    def select_one(self, condition):
        """
        :param condition: sql
        :return: 字典形式的单条查询结果
        """
        try:
            rows_affect = self.cur.execute(condition)
            if rows_affect > 0:
                results = self.cur.fetchone()  # 获取一条结果
                result = {'code': '0000', 'message': '执行操作成功', 'data': results}
            else:
                result = {'code': '0000', 'message': '执行操作成功', 'data': []}
        except pymysql.Error as e:
            self.conn.rollback()  # 回滚
            result = {'code': '9999', 'message': '执行操作异常', 'data': []}
            print('数据库错误|select_one %d: %s' % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + 'C:\\Users\\user\\Desktop\\test_interface\\syserror.log',
                                levell=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line: %(lineo)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result
