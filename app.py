from json import load
from rides.email.sender import send

with open('config/keys.json') as fp:
    config = load(fp)

email = config['email']
username = email['username']
password = email['password']

host = email['outbound']['host']
port = email['outbound']['port']


# send(host, port, username, password, '', 'this is a test message')

from rides.email.receiver import retrieve

inbound = config['email']['inbound']

retrieve(inbound['host'], username, password)