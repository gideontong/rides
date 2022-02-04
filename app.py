from imap_tools import MailMessage
from rides.email.sender import send
from rides.email.receiver import retrieve
from rides.nodes import person
from rides.util import (
    config, domains, people,
    marshal_person
)
from rides.util.email import process_email
from time import sleep
from typing import Dict, List


BACKOFF = 10


def periodic_loop(people: Dict[str, person]) -> None:
    phone_numbers = set(list(people))
    seen_emails = set()

    try:
        while True:
            emails: List[MailMessage] = retrieve(
                inbound['host'], username, password, phone_numbers)

            for email in emails:
                potential = marshal_person(email.from_, people)
                if potential:
                    name, number = potential
                else:
                    pass
                seen_emails, seen, text = process_email(seen_emails, email)

            exit()
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

    tracked_people: Dict[str, person] = dict()
    for person_ in people:
        next_person = person(person_)
        tracked_people[next_person.phone] = next_person

    periodic_loop(tracked_people)
