from rides.email.sender import send
from rides.email.receiver import retrieve
from rides.nodes import person
from rides.util import config, domains, people
from time import sleep


BACKOFF = 10


def periodic_loop(people: dict):
    try:    
        while True:
            sleep(BACKOFF)
    except KeyboardInterrupt:
        print('Program exit request by user. Exiting.')


if __name__ == '__main__':
    email = config['email']
    username = email['username']
    password = email['password']

    host = email['outbound']['host']
    port = email['outbound']['port']

    inbound = config['email']['inbound']

    mode = 'Sunday service'  # or Friday large group

    tracked_people = dict()
    for person_ in people:
        next_person = person(person_)
        tracked_people[next_person.phone] = next_person

    # periodic_loop(tracked_people)

    # retrieve(inbound['host'], username, password)
