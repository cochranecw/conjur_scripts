from requests.auth import HTTPBasicAuth
import base64
import requests
import os
import jwt


conjur_host = 'https://conjur'
user = 'admin'
org = 'myorg'
cert = './conjur-myorg.pem'

### endpoints ###
login_url = conjur_host + '/authn/' + org + '/login/'
#authenticate = conjur_host + /


def check_netrc():
    if os.path.isfile('~/.netrc'):
        return True
    else:
        return False


def create_file():
    return True


def login(host, account):
    url = host + '/authn/' + account + '/login/'
    response = requests.get(url, auth=HTTPBasicAuth(user, 'Cyberark1'), verify=cert)
    print("Successfully logged in and received API key for user admin: " + response.text)
    return response.text


def authenticate(host, user_id, account):
    api_key = login(host, account)
    url = host + '/authn/' + account + '/' + user_id + '/authenticate/'
    response = requests.post(url, data=api_key, verify=cert)
    r = response.json()
    print(base64.encodebytes(jwt.encode(r, None, None)))
    base64string = base64.encodebytes(('%s:%s:%s' % (r['protected'],r['payload'],r['signature'])).encode('utf8')).decode('utf8').replace('\n', '')
    #print("Successfully connected to authenticate and received auth token: " + response.json())
    return base64string



def create_hft(host, user_id, account):
    auth_token = authenticate(host, user_id, account)
    url = host + '/host_factory_tokens'
    data = 'expiration=2017-08-04T22:27:20+00:00', 'host_factory=myorg:host_factory:hf-db'
    headers = {'Authorization': 'Token token="' + auth_token + '"'}
    print(headers)
    response = requests.post(url, headers=headers, verify=cert)
    return response


def create_identity():
    return


menu_choice = input('(1) Create a Host Factory Token \
                   \n(2) Create an Identity \
                   \n(3) Exit \n')


if menu_choice == '1':
    print("Creating a host factory token...")
    print(create_hft(conjur_host, user, org))
elif menu_choice == '2':
    print("Creating an identity...")
elif menu_choice == '3':
    print("Exiting")
else:
    print("Please select another option")

