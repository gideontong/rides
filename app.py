from rides.email.sender import send
from rides.email.receiver import retrieve
from json import load


def start_moves(person: dict, mode: str):
    recipient = person['phone'] + '@' + domains[person['carrier']]
    send(host, port, username, password, recipient,
         f'Hi, {person["fname"]}!', f'Are you able to drive for {mode}? (yes/no)')


def next_move():
    pass


if __name__ == '__main__':
    with open('config/keys.json') as fp:
        config = load(fp)

    with open('config/domains.json') as fp:
        domains = load(fp)

    with open('config/people.json') as fp:
        people = load(fp)

    email = config['email']
    username = email['username']
    password = email['password']

    host = email['outbound']['host']
    port = email['outbound']['port']

    inbound = config['email']['inbound']

    mode = 'Sunday service'  # or Friday large group

    for person in people:
        start_moves(person, mode)

    # retrieve(inbound['host'], username, password)
