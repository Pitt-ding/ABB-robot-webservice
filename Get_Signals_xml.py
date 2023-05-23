#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : PR
# @Time     : 2023/5/14 10:07
# @File     : Get_Signals_xml.py
# @Project  : WebService

import requests
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as ET
import pymysql


Username = "Default User"
pass_word = "robotics"
NAMESPACE = '{http://www.w3.org/1999/xhtml}'


def xml_parse(_xml_str, _sql_log_fun):
    root = ET.fromstring(_xml_str)
    if root.findall(".//{}li[@class='ios-signal-li']".format(NAMESPACE)):
        list_findall = root.findall(".//{}li[@class='ios-signal-li']".format(NAMESPACE))
        print("{0:20s}: {1:10s}, {2:10s}, {3:10s}, {4:20s}".format(list_findall[0][1].attrib["class"],
                                                                   list_findall[0][2].attrib["class"],
                                                                   list_findall[0][3].attrib["class"],
                                                                   list_findall[0][4].attrib["class"],
                                                                   list_findall[0][5].attrib["class"]))
        for _index in list_findall:
            _list = [_index[x].text if _index[x].text is not None else 'None' for x in range(len(_index))]
            print("{0:20s}: {1:10s}, {2:10s}, {3:10s}, {4:20s}".format(_list[1],
                                                                       _list[2], _list[3], _list[4], _list[5]))
            _sql_log_fun(_list)


class SqlOperation:
    """
    common operation for sql
    """
    def __init__(self, _host="localhost", _user="root", _pass_word="root", _database="RobotSignals"):
        self.USER_NAME = _user
        self.PASSWORD = _pass_word
        self.HOST = _host
        self.DATABASE = _database
        self.COMMAND_INSERT = "INSERT INTO {}({})" \
                              " values " \
                              "{};"
        self.COMMAND_DROP = "Drop table {};"
        self.COMMAND_DELETE = "DELETE FROM {0} where {1} = '{2}';"
        self.COMMAND_SHOW_TABLE = "SHOW TABLES"
        self.COMMAND_USE_DATABASE = "SHOW DATABASES"
        self.COMMAND_USE_DATABASE = "USE {}"
        self.COMMAND_TRUNCATE_TABLE = "TRUNCATE table {};"
        self.COMMAND_UPDATE = "UPDATE {} SET {} where {}"
        self.COMMAND_CREATE_SIGNAL_TABLE = """create table if not exists `{}`({}
                                                PRIMARY KEY ( `{}` )\
                                            )ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

    def insert_data(self, _table_name: str, _column_name: str, _table_value: tuple) -> None:
        try:
            db = pymysql.connect(host=self.HOST, user=self.USER_NAME, password=self.PASSWORD, database=self.DATABASE)
        except:
            print('Insert data, Connect to sql failed!')
            return
        my_cursor = db.cursor()
        try:
            # print(self.COMMAND_INSERT.format(_table_name, _column_name, _table_value))
            my_cursor.execute(self.COMMAND_INSERT.format(_table_name, _column_name, _table_value))
            db.commit()
            print('Insert data done!')
        except:
            db.rollback()
            print('Insert data failed!')
        db.close()

    def update_data(self, _table_name: str, _set_value: str, _where_value: str) -> None:
        try:
            db = pymysql.connect(host=self.HOST, user=self.USER_NAME, password=self.PASSWORD, database=self.DATABASE)
        except:
            print('Update data, Connect to sql failed!')
            return
        my_cursor = db.cursor()
        try:
            print(self.COMMAND_UPDATE.format(_table_name, _set_value, _where_value))
            my_cursor.execute(self.COMMAND_UPDATE.format(_table_name, _set_value, _where_value))
            db.commit()
            print('Update data done!')
        except:
            db.rollback()
            print('update data failed!')
        db.close()

    def delete_data(self, _table_name: str, _column_name: str, _value: str) -> None:
        try:
            db = pymysql.connect(host=self.HOST, user=self.USER_NAME, password=self.PASSWORD, database=self.DATABASE)
        except:
            print('Delete data, Connect to sql failed!')
            return

        my_cursor = db.cursor()
        try:
            my_cursor.execute(self.COMMAND_DELETE.format(_table_name, _column_name, _value))
            db.commit()
            print('Delete data Done!')
        except:
            db.rollback()
            print('Delete data failed!')
        db.close()

    def show_table(self) -> None:
        try:
            db = pymysql.connect(host=self.HOST, user=self.USER_NAME, password=self.PASSWORD, database=self.DATABASE)
        except:
            print('Show table, Connect to sql failed!')
            return
        my_cursor = db.cursor()
        my_cursor.execute(self.COMMAND_SHOW_TABLE)
        for _i in my_cursor.fetchall():
            print("data table: {}".format(_i[0]))

    def create_table(self, _table_name: str, _column_name: str, _primary_key: str) -> None:
        try:
            db = pymysql.connect(host=self.HOST, user=self.USER_NAME, password=self.PASSWORD, database=self.DATABASE)
        except:
            print('Create table, Connect to sql failed!')
            return
        my_cursor = db.cursor()
        try:
            # print(self.COMMAND_CREATE_SIGNAL_TABLE.format(_table_name, _column_name, _primary_key))
            my_cursor.execute(self.COMMAND_CREATE_SIGNAL_TABLE.format(_table_name, _column_name, _primary_key))
            db.commit()
        except:
            print("Create table failed!")
            db.rollback()
        db.close()

    def drop_table(self, _table_name: str) -> None:
        try:
            db = pymysql.connect(host=self.HOST, user=self.USER_NAME, password=self.PASSWORD, database=self.DATABASE)
        except:
            print('Update data, Connect to sql failed!')
            return
        my_cursor = db.cursor()
        try:
            my_cursor.execute(self.COMMAND_DROP.format(_table_name))
            db.commit()
            print('Drop data done!')
        except:
            db.rollback()
        db.close()

    def truncate_table(self, _table_name: str) -> None:
        try:
            db = pymysql.connect(host=self.HOST, user=self.USER_NAME, password=self.PASSWORD, database=self.DATABASE)
        except:
            print('truncate table, Connect to sql failed!')
            return
        my_cursor = db.cursor()
        try:
            my_cursor.execute(self.COMMAND_TRUNCATE_TABLE.format(_table_name))
            print('Truncate table Done!')
        except:
            db.rollback()
            print('Truncate table failed!')
        db.close()

    def parse_tuple(self, _tuple: tuple) -> str:
        _string = "("
        for _i in range(len(_tuple)):
            if _i < len(_tuple)-1:
                _string += _tuple[_i] + ","
            else:
                _string += _tuple[_i]
        _string += ")"
        print(_string)
        return _string


if __name__ == '__main__':
    my_sql = SqlOperation()
    digit_httpauth = HTTPDigestAuth(Username, pass_word)
    result_xml = requests.get(url="http://127.0.0.1/rw/iosystem/signals", auth=digit_httpauth)
    print("___")
    # if result_xml.status_code == 200:
    #     print(result_xml.text)
    #     xml_parse(result_xml.text, my_sql.insert_data)
    # else:
    #     print("wrong status code {}: ".format(result_xml.status_code))
    # my_sql.show_table('robotsignals')

    # sql 常用sql创建表及更新数据指令-----------------------------------------------------------------
    # my_sql.create_table("""table_name""", """
    # `id` INT UNSIGNED AUTO_INCREMENT,
    # `name` VARCHAR(100),
    # `type` VARCHAR(100),
    # `category` VARCHAR(40),
    # `lvalue` varchar(40),
    # `lstate` varchar(40),""", """id""")
    my_sql.insert_data("table_name", """name,type,category,lvalue,lstate""", ('pitt', 'int', 'None', '2', 'No simulate'))
    # my_sql.update_data("table_name", "lvalue= '5'", "name = 'pitt'")
    # my_sql.delete_data('table_name', 'lvalue', '5')
    # my_sql.drop_table("table_name")
    # my_sql.show_table()
    # my_sql.truncate_table("table_name")








