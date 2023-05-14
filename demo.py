#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : PR
# @Time     : 2023/5/11 23:50
# @File     : demo.py
# @Project  : WebService
import xml.etree.ElementTree as ET

xml_file = """<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml"> <head> <title>Event</title><base href="http://127.0.0.1:80/"/> </head> <body>"  <div class="state"><a href="subscription/6" rel="group"></a> <ul> <li class="pnl-speedratio-ev" title="speedratio"><a href="/rw/panel/speedratio" rel="self"></a><span class="speedratio">50</span></li>  </ul> </div> </body></html>"""
if __name__ == '__main__':
    namespace = '{http://www.w3.org/1999/xhtml}'
    root = ET.fromstring(xml_file)
    # print("\tSpeed Ratio : " + root.find(".//{0}li[@class='pnl-speedratio-ev']/{0}span".format(namespace)).text)
    print(root.find(".//{0}span".format(namespace)).text)


