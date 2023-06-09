import xml.etree.ElementTree as ET
from ws4py.client.threadedclient import WebSocketClient
import requests
from requests.auth import HTTPDigestAuth

USER_NAME = "Default User"
PASSWORD = "robotics"
HOST = "127.0.0.1:80"
NAMESPACE = '{http://www.w3.org/1999/xhtml}'


def print_event(evt):
    root = ET.fromstring(evt)
    print(type(evt))
    # print(evt)
    if root.findall(".//{0}li[@class='pnl-ctrlstate-ev']".format(NAMESPACE)):
        print("\tController State : " + root.find(".//{0}li[@class='pnl-ctrlstate-ev']/{0}span".format(NAMESPACE)).text)
    if root.findall(".//{0}li[@class='pnl-opmode-ev']".format(NAMESPACE)):
        print("\tOperation Mode : " + root.find(".//{0}li[@class='pnl-opmode-ev']/{0}span".format(NAMESPACE)).text)
    if root.findall(".//{0}li[@class='pnl-speedratio-ev']".format(NAMESPACE)):
        print("\tSpeed Ratio : " + root.find(".//{0}li[@class='pnl-speedratio-ev']/{0}span".format(NAMESPACE)).text)
    if root.findall(".//{0}li[@class='ios-signalstate-ev']".format(NAMESPACE)):
        print("\tdo_ws_signal : " + root.find(".//{0}li[@class='ios-signalstate-ev']/{0}span[@class='lvalue']".format(NAMESPACE)).text)


# This class encapsulates the Web Socket Callbacks functions.
class RobWebSocketClient(WebSocketClient):
    def opened(self):
        print("Web Socket connection established")

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, event_xml):
        if event_xml.is_text:
            print("Events : ")
            # print(event_xml)
            print_event(event_xml.data.decode("utf-8"))
        else:
            print("Received Illegal Event " + str(event_xml))


# The main RobotWare Panel class
class RWPanel:

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.digest_auth = HTTPDigestAuth(self.username, self.password)
        self.subscription_url = 'http://{0}/subscription'.format(self.host)
        self.session = requests.Session()

    def subscribe(self):
        # Create a payload to subscribe on RobotWare Panel Resources with high priority
        payload = {'resources': ['1', '2', '3', '4'],
                   '1': '/rw/panel/speedratio',
                   '1-p': '1',
                   '2': '/rw/iosystem/signals/do_ws_signal;state',
                   '2-p': '1',
                   '3': '/rw/panel/opmode',
                   '3-p': '1',
                   '4': '/rw/panel/ctrlstate',
                   '4-p': '1'
                   }
        # payload = {"resources": "1", "1": "/rw/iosystem/signals/do_ws_signal;state", "1-p": "1"}

        resp = self.session.post(self.subscription_url, auth=self.digest_auth, data=payload)
        print("Initial Events : ")
        print_event(resp.text)
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

# def enable_http_debug():
#     import logging
    # import httplib
    # httplib.HTTPConnection.debuglevel = 1
    # logging.basicConfig()  # Initialize logging
    # logging.getLogger().setLevel(logging.DEBUG)
    # requests_log = logging.getLogger("requests.packages.urllib3")
    # requests_log.setLevel(logging.DEBUG)
    # requests_log.propagate = True


# def main(argv):
#     try:
#         parser = argparse.ArgumentParser()
#         parser.add_argument("-host", help="The host to connect. Defaults to localhost on port 80",
#                             default='localhost:80')
#         parser.add_argument("-user", help="The login user name. Defaults to default user name", default='Default User')
#         parser.add_argument("-passcode", help="The login password. Defaults to default password", default='robotics')
#         parser.add_argument("-debug", help="Enable HTTP level debugging.", action='store_true')
#         args = parser.parse_args()
#
#         if args.debug:
#             enable_http_debug()
#
#         rwpanel = RWPanel(args.host, args.user, args.passcode)
#         if rwpanel.subscribe():
#             rwpanel.start_recv_events()
#     except KeyboardInterrupt:
#         rwpanel.close()

if __name__ == "__main__":
    # main(sys.argv[1:])
    myRw = RWPanel(HOST, USER_NAME, PASSWORD)
    print(myRw.subscribe())
    print(myRw.start_recv_events())

