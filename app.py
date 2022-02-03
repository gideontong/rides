from json import load
from rides.email.sender import send

with open('config/keys.json') as fp:
    keys = load(fp)

host = keys['email']['outbound']['host']
username = keys['email']['username']
password = keys['email']['password']


send(host, username, password, '', 'this is a test message')