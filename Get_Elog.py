#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : PR
# @Time     : 2023/5/13 18:24
# @File     : Get_Elog.py
# @Project  : WebService

import requests
from requests.auth import HTTPDigestAuth
from typing import Union

Username = "Default User"
pass_word = "robotics"

if __name__ == '__main__':

    digit_httpauth = HTTPDigestAuth(Username, pass_word)
    result_json = requests.get(url="http://127.0.0.1/rw/elog/0?lang=en", auth=digit_httpauth)

    print("___")
    print(result_json.content)






