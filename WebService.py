#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : PR
# @Time     : 2023/5/23 19:12
# @File     : WebService.py
# @Project  : WebService

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : PR
# @Time     : 2023/5/23 12:45
# @File     : WebService.py
# @Project  : ShineRobot

import requests
import time
from requests.auth import HTTPDigestAuth
from typing import Union
import xml.etree.ElementTree as ET
from ws4py.client.threadedclient import WebSocketClient
import requests
from requests.auth import HTTPDigestAuth


class WebService:
    def __init__(self, _ip: str = "127.0.0.1") -> None:
        self.get_result = None
        self.digit_httpauth = None
        self.NAMESPACE = '{http://www.w3.org/1999/xhtml}'
        self.PASS_WORD = "robotics"
        self.USER_NAME = "Default User"
        self.PAY_LOAD = {'lvalue': '1'}
        self.PAY_LOAD_FALSE = {'lvalue': '0'}
        self.SERVER_IP = _ip
        self.SERVER_PORT = "80"
        self.PAYLOAD = {'resources': ['1', '2', '3', '4'],
                        '1': '/rw/panel/speedratio',
                        '1-p': '1',
                        '2': '/rw/iosystem/signals/do_ws_signal;state',
                        '2-p': '1',
                        '3': '/rw/panel/opmode',
                        '3-p': '1',
                        '4': '/rw/panel/ctrlstate',
                        '4-p': '1'
                        }
        # self.SERVER_URL = "http://{}:{}/rw/iosystem/signals/do_ws_signal?action=set".format(SERVER_IP, SERVER_PORT)

    def get(self, _url: str) -> str:
        digit_httpauth = HTTPDigestAuth(self.USER_NAME, self.PASS_WORD)
        self.get_result = requests.get(url='http://{}:{}'.format(self.SERVER_IP, self.SERVER_PORT) + _url, auth=digit_httpauth)
        if self.get_result.status_code == 400:
            return 'request get failed'
        elif self.get_result.status_code == 404:
            return 'request get page could not be found'
        else:
            return self.get_result.text

    def post(self, _url: str, _lvalue: Union[bool, int]) -> str:
        if isinstance(_lvalue,bool):
            _pay_load = {'lvalue': '{}'.format(str(_lvalue))}
        elif isinstance(_lvalue, int):
            _pay_load = {'lvalue': '{}'.format(str(_lvalue))}
        else:
            return False
        # using HTTPDigestAuth to generate digest credentials
        self.digit_httpauth = HTTPDigestAuth(self.USER_NAME, self.PASS_WORD)
        # initial the post cookies with first post command
        result_json = requests.post(url='http://{}:{}'.format(self.SERVER_IP, self.SERVER_PORT) + _url, auth=self.digit_httpauth, data=_pay_load)
        # result_json = requests.post(url=SERVER_URL, auth=self.digit_httpauth, data=PAY_LOAD_TRUE,
        #                             cookies=result_json.cookies)
        # judge set status by status code
        if result_json.status_code == 204:
            return 'Request success'
        else:
            return 'Request failed'

    def subscribe(self, _pay_load):
        my_rw = RWPanel(self.SERVER_IP, self.SERVER_PORT, self.USER_NAME, self.PASS_WORD)
        if my_rw.subscribe(_pay_load):
            print(my_rw.start_recv_events())
        else:
            print('subscribe failed')


# The main RobotWare Panel class
class RWPanel:
    def __init__(self, _ip: str, _port: str, _username: str, _password: str) -> None:
        self.host = _ip + ':' + _port
        self.username = _username
        self.password = _password
        self.digest_auth = HTTPDigestAuth(self.username, self.password)
        self.subscription_url = 'http://{0}/subscription'.format(self.host)
        self.session = requests.Session()

    def subscribe(self, _pay_load):
        # Create a payload to subscribe on RobotWare Panel Resources with high priority
        resp = self.session.post(self.subscription_url, auth=self.digest_auth, data=_pay_load)
        print("Initial Events : ")
        # print(resp.text)
        if resp.status_code == 201:
            self.location = resp.headers['Location']
            self.cookie = '-http-session-={0}; ABBCX={1}'.format(resp.cookies['-http-session-'], resp.cookies['ABBCX'])
            return True
        else:
            print('Error subscribing ' + str(resp.status_code))
            return False

    def start_recv_events(self):
        self.header = [('Cookie', self.cookie)]
        self.ws = RobWebSocketClient(self.location,
                                     protocols=['robapi2_subscription'],
                                     headers=self.header)
        self.ws.connect()
        self.ws.run_forever()

    def close(self):
        self.ws.close()


class RobWebSocketClient(WebSocketClient):
    def opened(self):
        print("Web Socket connection established")

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, event_xml):
        if event_xml.is_text:
            print("Events : ")
            self.print_event(event_xml.data.decode("utf-8"))
        else:
            print("Received Illegal Event " + str(event_xml))

    @staticmethod
    def print_event(_evt):
        NAMESPACE = '{http://www.w3.org/1999/xhtml}'
        root = ET.fromstring(_evt)
        # print(type(evt))
        if root.findall(".//{0}li[@class='pnl-ctrlstate-ev']".format(NAMESPACE)):
            print("\tController State : " + root.find(".//{0}li[@class='pnl-ctrlstate-ev']/{0}span".format(NAMESPACE)).text)
        if root.findall(".//{0}li[@class='pnl-opmode-ev']".format(NAMESPACE)):
            print("\tOperation Mode : " + root.find(".//{0}li[@class='pnl-opmode-ev']/{0}span".format(NAMESPACE)).text)
        if root.findall(".//{0}li[@class='pnl-speedratio-ev']".format(NAMESPACE)):
            print("\tSpeed Ratio : " + root.find(".//{0}li[@class='pnl-speedratio-ev']/{0}span".format(NAMESPACE)).text)
        if root.findall(".//{0}li[@class='ios-signalstate-ev']".format(NAMESPACE)):
            print("\tdo_ws_signal : " + root.find(".//{0}li[@class='ios-signalstate-ev']/{0}span[@class='lvalue']".format(NAMESPACE)).text)


if __name__ == '__main__':
    my_webservice = WebService()
    print(my_webservice.get('/rw/iosystem/signals'))
    # print_event(my_webservice.get('/rw/iosystem/signals'))
    print(my_webservice.post(_url='/rw/iosystem/signals/do_ws_signal?action=set', _lvalue=1))
    my_webservice.subscribe({'resources': ['1', '2', '3', '4'],
                        '1': '/rw/panel/speedratio',
                        '1-p': '1',
                        '2': '/rw/iosystem/signals/do_ws_signal;state',
                        '2-p': '1',
                        '3': '/rw/panel/opmode',
                        '3-p': '1',
                        '4': '/rw/panel/ctrlstate',
                        '4-p': '1'
                        })

