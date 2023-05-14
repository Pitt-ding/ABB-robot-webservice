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
    def __init__(self, _host="localhost", _user="root", _pass_word="root", _database="RobotSignals"):
        self.USER_NAME = _user
        self.PASSWORD = _pass_word
        self.HOST = _host
        self.DATABASE = _database
        self.COMMAND_INSERT = "INSERT INTO RobotSignals.signal_table(name, type, category, lvalue, lstate)" \
                              " values " \
                              "('{1:s}', '{2:s}', '{3:s}', '{4:s}', '{5:s}');"
        self.COMMAND_DROP = "Drop table {};"
        self.COMMAND_DELETE = "DELETE FROM {0} where {1} = '{2}';"
        self.COMMAND_SHOW_TABLE = "SHOW TABLES"
        self.COMMAND_USE_DATABASE = "SHOW DATABASES"
        self.COMMAND_USE_DATABASE = "USE {}"
        self.COMMAND_TRUNCATE_TABLE = "TRUNCATE table {};"
        self.COMMAND_CREATE_SIGNAL_TABLE = "create table if not exists `signal_table`(\
                                                `id` INT UNSIGNED AUTO_INCREMENT,\
                                                `name` VARCHAR(100),\
                                                `type` VARCHAR(100),\
                                                `category` VARCHAR(40),\
                                                `lvalue` varchar(40),\
                                                `lstate` varchar(40),\
                                                PRIMARY KEY ( `id` )\
                                            )ENGINE=InnoDB DEFAULT CHARSET=utf8;"

    def insert_data(self, _log_value):
        db = pymysql.connect(host=self.HOST, user=self.USER_NAME, password=self.PASSWORD, database=self.DATABASE)
        my_cursor = db.cursor()
        my_cursor.execute(self.COMMAND_INSERT.format(*_log_value))
        db.commit()

    def update_data(self, _log_value):
        db = pymysql.connect(host=self.HOST, user=self.USER_NAME, password=self.PASSWORD, database=self.DATABASE)
        my_cursor = db.cursor()
        my_cursor.execute(self.COMMAND_INSERT.format(*_log_value))
        db.commit()

    def drop_table(self, _table_name):
        db = pymysql.connect(host=self.HOST, user=self.USER_NAME, password=self.PASSWORD, database=self.DATABASE)
        my_cursor = db.cursor()
        my_cursor.execute(self.COMMAND_DROP.format(_table_name))
        db.commit()

    def delete_data(self, _table_name, _column_name, _value):
        db = pymysql.connect(host=self.HOST, user=self.USER_NAME, password=self.PASSWORD, database=self.DATABASE)
        my_cursor = db.cursor()
        my_cursor.execute(self.COMMAND_DELETE.format(_table_name, _column_name, _value))
        db.commit()

    def show_table(self):
        db = pymysql.connect(host=self.HOST, user=self.USER_NAME, password=self.PASSWORD, database=self.DATABASE)
        my_cursor = db.cursor()
        # my_cursor.execute(self.COMMAND_USE_DATABASE.format(_database))
        my_cursor.execute(self.COMMAND_SHOW_TABLE)
        for _i in my_cursor.fetchall():
            print("data table: {}".format(_i[0]))

    def create_table(self):
        db = pymysql.connect(host=self.HOST, user=self.USER_NAME, password=self.PASSWORD, database=self.DATABASE)
        my_cursor = db.cursor()
        my_cursor.execute(self.COMMAND_CREATE_SIGNAL_TABLE)

    def truncate_table(self, _table_name):
        db = pymysql.connect(host=self.HOST, user=self.USER_NAME, password=self.PASSWORD, database=self.DATABASE)
        my_cursor = db.cursor()
        my_cursor.execute(self.COMMAND_TRUNCATE_TABLE.format(_table_name))


if __name__ == '__main__':
    my_sql = SqlOperation()
    digit_httpauth = HTTPDigestAuth(Username, pass_word)
    result_xml = requests.get(url="http://127.0.0.1/rw/iosystem/signals", auth=digit_httpauth)
    print("___")
    if result_xml.status_code == 200:
        print(result_xml.text)
        xml_parse(result_xml.text, my_sql.insert_data)
    else:
        print("wrong status code {}: ".format(result_xml.status_code))
    # my_sql.show_table('robotsignals')






