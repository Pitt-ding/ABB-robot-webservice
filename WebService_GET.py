import requests
from requests.auth import HTTPDigestAuth
from typing import Union

Username = "Default User"
pass_word = "robotics"

if __name__ == '__main__':

    digit_httpauth = HTTPDigestAuth(Username, pass_word)
    result_json = requests.get(url="http://127.0.0.1/rw/iosystem/signals?json=1", auth=digit_httpauth)
    str_json = result_json.json()
    print("___")


    def iter_json(_seq: Union[dict, list]) -> None:
        if isinstance(_seq, dict):
            for _index in _seq:
                if isinstance(_seq[_index], (dict, list)):
                    iter_json(_seq[_index])
                else:
                    if _index == "option":
                        # print(type(_seq[_index]))
                        print("{}: {}".format(_index, _seq[_index]))
                    elif _index == "_title":
                        print("{}: {}".format(_index, _seq[_index]))
        elif isinstance(_seq, list):
            for _index in range(len(_seq)):
                if isinstance(_seq[_index], (dict, list)):
                    iter_json(_seq[_index])
                else:
                    print("{}: {}".format(_index, _seq[_index]))

    iter_json(str_json)




