#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : PR
# @Time     : 2023/5/11 23:50
# @File     : demo.py
# @Project  : WebService
import xml.etree.ElementTree as ET
import pymysql

xml_file = """<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml"> <head> <title>Event</title><base href="http://127.0.0.1:80/"/> </head> <body>"  <div class="state"><a href="subscription/6" rel="group"></a> <ul> <li class="pnl-speedratio-ev" title="speedratio"><a href="/rw/panel/speedratio" rel="self"></a><span class="speedratio">50</span></li>  </ul> </div> </body></html>"""
t1 = ('name', 'type', 'category', 'lvalue', 'lstate')
# name, type, category, lvalue, lstate '{{1:s}', '{2:s}', '{3:s}', '{4:s}', '{5:s}} {} {} {} {} {}
TABLE_NAME = "RobotSignals.signal_table"
COLUMN = t1
TABLE_VALUE = ("1", "2", "3", "4", "5")
COMMAND_INSERT = """INSERT INTO {} {} \
                              values \
                              {};"""


class SqlOperation:
    def __init__(self, _host="localhost", _user="root", _pass_word="root", _database="RobotSignals"):
        self.USER_NAME = _user
        self.PASSWORD = _pass_word
        self.HOST = _host
        self.DATABASE = _database
        self.COMMAND_INSERT = """INSERT INTO {} {} \
                              values \
                              {};"""
        self.COMMAND_DROP = "Drop table {};"
        self.COMMAND_DELETE = "DELETE FROM {0} where {1} = '{2}';"
        self.COMMAND_SHOW_TABLE = "SHOW TABLES"
        self.COMMAND_USE_DATABASE = "SHOW DATABASES"
        self.COMMAND_USE_DATABASE = "USE {}"
        self.COMMAND_TRUNCATE_TABLE = "TRUNCATE table {};"
        self.COMMAND_UPDATE = "UPDATE {} SET {} where name={}"
        self.COMMAND_CREATE_SIGNAL_TABLE = "create table if not exists `signal_table`(\
                                                `id` INT UNSIGNED AUTO_INCREMENT,\
                                                `name` VARCHAR(100),\
                                                `type` VARCHAR(100),\
                                                 `category` VARCHAR(40),\
                                                `lvalue` varchar(40),\
                                                `lstate` varchar(40),\
                                                PRIMARY KEY ( `id` )\
                                            )ENGINE=InnoDB DEFAULT CHARSET=utf8;"

    def create_table(self):
        db = pymysql.connect(host=self.HOST, user=self.USER_NAME, password=self.PASSWORD, database=self.DATABASE)
        my_cursor = db.cursor()
        print(self.COMMAND_INSERT.format(TABLE_NAME, self.parse_tuple(COLUMN), TABLE_VALUE))
        my_cursor.execute(self.COMMAND_INSERT.format(TABLE_NAME, self.parse_tuple(COLUMN), TABLE_VALUE))
        db.commit()


    def parse_tuple(self, _tuple):
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
    namespace = '{http://www.w3.org/1999/xhtml}'
    root = ET.fromstring(xml_file)
    # print("\tSpeed Ratio : " + root.find(".//{0}li[@class='pnl-speedratio-ev']/{0}span".format(namespace)).text)
    print(root.find(".//{0}span".format(namespace)).text)
    print(type(t1))
    print("string of tuple: "+str(t1))
    # parse_tuple(COLUMN)

    print("({}, {}, {}, {}, {})".format(*t1))
    # print(COMMAND_INSERT.format(TABLE_NAME, parse_tuple(COLUMN), TABLE_VALUE))
    my_sql = SqlOperation()
    my_sql.create_table()



