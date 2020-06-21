# -*- coding:utf-8 -*-
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
            logging.basicConfig(filename=config.src_path + 'C:\\Users\\user\\Desktop\\test_interface\\log\\syserror.log',
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line: %(lineo)d]%(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)

    # 定义单条数据操作，包含删除、更新操作
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
            logging.basicConfig(filename=config.src_path + 'C:\\Users\\user\\Desktop\\test_interface\\log\\syserror.log',
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line: %(lineo)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    # 查询表中单条数据
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
            logging.basicConfig(filename=config.src_path + 'C:\\Users\\user\\Desktop\\test_interface\\log\\syserror.log',
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line: %(lineo)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    # 查询表中多条数据
    def select_all(self, condition):
        """
        :param condition: sql
        :return: 字典形式的批量查询结果
        """
        try:
            rows_affect = self.cur.execute(condition)
            if rows_affect > 0:
                self.cur.scroll(0, mode='absolute')  # 鼠标回到最初位置
                results = self.cur.fetchall()  # 返回游标中所有的结果
                result = {'code': '0000', 'message': '执行操作成功', 'data': results}
            else:
                result = {'code': '0000', 'message': '执行操作成功', 'data': []}
        except pymysql.Error as e:
            self.conn.rollback()  # 回滚
            result = {'code': '9999', 'message': '执行操作异常', 'data': []}
            logging.basicConfig(filename=config.src_path + 'C:\\Users\\user\\Desktop\\test_interface\\log\\syserror.log',
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line: %(lineo)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    # 定义表中插入数据操作
    def insert_data(self, condition, params):
        """

        :param condition: insert语句
        :param params: insert数据，列表形式[('3','tom'),('2', 'jack')]
        :return: 字典形式的批量插入数据结果
        """
        try:
            results = self.cur.executemany(condition, params)
            self.conn.commit()
            result = {'code': '0000', 'message': '执行操作成功', 'data': results}
        except pymysql.Error as e:
            self.conn.rollback()  # 回滚
            result = {'code': '9999', 'message': '执行操作异常', 'data': []}
            logging.basicConfig(filename=config.src_path + 'C:\\Users\\user\\Desktop\\test_interface\\log\\syserror.log',
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line: %(lineo)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    # 关闭数据库
    def __del__(self):
        if self.cur is not None:
            self.cur.close()  # 关闭游标
        if self.conn is not None:
            self.conn.close()


if __name__ == '__main__':
    test = OperationDbInterface()
    result_select_all = test.select_all("SELECT * FROM config_total")
    result_select_one = test.select_one("SELECT * FROM config_total WHERE id=1")
    result_op_sql = test.op_sql("UPDATE config_total set value_config='test' WHERE id=1")
    result = test.insert_data("insert into config_total(key_config, value_config, description, status) values (%s, %s, %s, %s)",
                              [('mytest1', 'mytest11', 'ceshi', 1), ('mytest2', 'mytest22', 'ceshi22', 2)])
    print(result_select_all['data'], result_select_all['message'])
    print(result_select_one['data'], result_select_one['message'])
    print(result_op_sql['data'], result_op_sql['message'])
    print(result['data'], result['message'])
