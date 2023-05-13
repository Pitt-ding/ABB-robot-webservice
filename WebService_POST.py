import time
import requests
from requests.auth import HTTPDigestAuth

USER_NAME = "Default User"
PASSWORD = "robotics"
PAY_LOAD_TRUE = {'lvalue': '1'}
PAY_LOAD_FALSE = {'lvalue': '0'}
SERVER_IP = "127.0.0.1"
SERVER_PORT = "80"
SERVER_URL = "http://{}:{}/rw/iosystem/signals/do_ws_signal?action=set".format(SERVER_IP, SERVER_PORT)

if __name__ == '__main__':
    # using HTTPDigestAuth to generate digest credentials
    digit_httpauth = HTTPDigestAuth(USER_NAME, PASSWORD)
    # initial the post cookies with first post command
    result_json = requests.post(url=SERVER_URL, auth=digit_httpauth, data=PAY_LOAD_TRUE)
    _index = 0
    while _index < 10:
        result_json = requests.post(url=SERVER_URL, auth=digit_httpauth, data=PAY_LOAD_TRUE, cookies=result_json.cookies)
        # judge set status by status code
        if result_json.status_code == 204:
            print("{} Signal success set".format(_index))
        else:
            print("{} Signal set failed".format(_index))
            break
        time.sleep(1)

        result_json = requests.post(url=SERVER_URL, auth=digit_httpauth, data=PAY_LOAD_FALSE, cookies=result_json.cookies)
        if result_json.status_code == 204:
            print("{} Signal success set".format(_index))
        else:
            print("{} Signal set failed".format(_index))
            break

        time.sleep(1)
        _index += 1

