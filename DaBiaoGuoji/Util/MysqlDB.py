import pymysql.cursors
import sys
from contextlib import contextmanager
import traceback
#import ExcelHelp as excel
import xlrd
import xlwt

from logbook import Logger, StreamHandler

StreamHandler(sys.stdout).push_application()
log = Logger('FileOperation')

"""
    pymysql.Connect()参数说明
    host(str):      MySQL服务器地址
    port(int):      MySQL服务器端口号
    user(str):      用户名
    passwd(str):    密码
    db(str):        数据库名称
    charset(str):   连接编码

    connection对象支持的方法
    cursor()        使用该连接创建并返回游标
    commit()        提交当前事务
    rollback()      回滚当前事务
    close()         关闭连接

    cursor对象支持的方法
    execute(op)     执行一个数据库的查询命令
    fetchone()      取得结果集的下一行
    fetchmany(size) 获取结果集的下几行
    fetchall()      获取结果集中的所有行
    rowcount()      返回数据条数或影响行数
    close()         关闭游标对象

"""


# charset='utf8'
class Mysql(object):
    StreamHandler(sys.stdout).push_application()
    logger = Logger('Mysql')
    # 连接数据库

    # 生产环境数据库
    __config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'db': 'yilongspider',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor,
    }

    # 数据库构造函数，从连接池中取出连接，并生成操作游标
    def __init__(self):
        """
        配置成员变量
        """
        # 连接对象
        self.__conn = self.__getConn()
        self.__cursor = self.__getCursor()

    def __getConn(self):
        """
        获取con连接
        :return:  con
        """
        self.__conn = pymysql.Connect(**Mysql.__config)
        return self.__conn

    def __getCursor(self):
        """
        获取游标
        :return: cursor
        """
        self.__cursor = self.__conn.cursor()
        return self.__cursor

    @contextmanager
    def __con_cursor(self):
        """
        1、定义上下文管理器，连接后自动关闭连接
        2、元组对象前面如果不带“*”、字典对象如果前面不带“**”，则作为普通的对象传递参数。
        :return:
        """
        # 打开连接
        conn = self.__getConn()
        # 打开游标
        cursor = self.__getCursor()

        try:
            yield cursor
        except Exception as ex:
            conn.rollback()
            Mysql.logger.error(repr(ex))
        finally:
            self.__conn.commit()
            self.__cursor.close()
            self.__conn.close()

    # ---------- 搜索 ----------

    def __query(self, cursor, sql, param=None):
        if param:
            count = cursor.execute(sql, param)
        else:
            count = cursor.execute(sql)
        return count

    def getOne(self, sql, param=None):
        """
        @summary: 执行查询，并取出第一条
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """

        with self.__con_cursor() as cursor:
            if self.__query(cursor, sql, param) > 0:
                result = cursor.fetchone()
            else:
                result = False
            return result

    def getMany(self, sql, param=None, num=1):
        """
        @summary: 执行查询，并取出num条结果
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num:取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        with self.__con_cursor() as cursor:
            if self.__query(cursor, sql, param) > 0:
                result = cursor.fetchmany(num)
            else:
                result = False
            return result

    def getAll(self, sql, param=None):
        """
        @summary: 执行查询，并取出所有结果集
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list(字典对象)/boolean 查询到的结果集
        """

        with self.__con_cursor() as cursor:
            if self.__query(cursor, sql, param) > 0:
                result = cursor.fetchall()
            else:
                result = False
            return result

    def __select(self, table, cond_dict=None, order=None):
        """
        @summary: 执行条件查询，并取出所有结果集
        @cond_dict:{'name':'xiaoming'...}
        @order:'order by id desc'
        @return:  result ({"col":"val","":""},{})
        """
        consql = ' '
        if cond_dict != '':
            for k, v in cond_dict.items():
                consql = consql + k + '=' + v + ' and'
        consql = consql + ' 1=1 '
        sql = 'select * from %s where ' % table
        sql = sql + consql + order
        print('_select:' + sql)
        return self.exeCute(sql)

    # ---------- 更新 ----------

    def update(self, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        with self.__con_cursor() as cursor:
            return cursor.execute(sql, param)

    # ---------- 删除 ----------

    def delete(self, sql, param=None):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """

        with self.__con_cursor() as cursor:
            return cursor.execute(sql, param)

    # ---------- 插入 ----------

    # 插入一条/多条数据
    def insert(self, sql, param):
        """
        @summary: 向数据表插入一条记录
        @param sql:要插入的ＳＱＬ格式
        @param value:要插入的记录数据tuple/list
        @return: insertId
        """
        with self.__con_cursor() as cursor:
            # 执行插入操作
            cursor.executemany(sql, param)
            # cursor.execute(sql)
            # 获取最后更新的ID
            return cursor.lastrowid


#if __name__ == '__main__':
    #aaa = Mysql()
    # print(aaa.getOne("select * from erp_users"))
    # print(aaa.getOne("select * from erp_users WHERE id in(%s)", (19,)))
    # for item in aaa.getMany("select * from erp_users WHERE id in(19,39)", None, 5):
    #     print(item)
    # for item in aaa.getAll("select name from erp_users ORDER BY `name` asc"):
    #     print(item)
    # for item in aaa.getAll("select * from erp_users WHERE id in(%s)", (19,)):
    #     print(item)
   # print(aaa.update("UPDATE erp_users SET mail =%s WHERE id = %s", ('123@789', 19)))
    # print(aaa.delete("DELETE erp_users WHERE id = %s", (19,)))
    # print(aaa.getInsertId())
    # 插入一条数据
    # print(aaa.insert("INSERT `erp_areas` (`areaName`,`charge`,`areaCode`,`is_delete`,`commission`) VALUES (%s,%s,%s,%s,%s)", ('通州片区2222ssssssd', '片区经理3', '0', '0', '0.90')))
    # 插入多条数据
    # print(aaa.insert("INSERT `erp_areas` (`areaName`,`charge`,`areaCode`,`is_delete`,`commission`) VALUES (%s,%s,%s,%s,%s)", ('通州片区2222ssssssd', '片区经理3', '0', '0', '0.90'), ('通州片区2222ssssssd', '片区经理3', '0','0', '0.90')))