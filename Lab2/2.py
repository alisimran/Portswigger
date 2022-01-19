import http
import requests
import sys
import urllib3
from bs4 import BeautifulSoup


proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
url = 'https://ace11f551eb9ca7ac085c7a300d900d4.web-security-academy.net/login'
username = 'administrator'
password = 'sdfs'



s = requests.Session()
response = s.get(url, auth=(username, password), verify=False, proxies=proxies)
print(response.text)