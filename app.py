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
from typing import Dict, List, Tuple


BACKOFF = 10

EMAIL = config['email']
USERNAME = EMAIL['username']
PASSWORD = EMAIL['password']

HOST = EMAIL['outbound']['host']
PORT = EMAIL['outbound']['port']

INBOUND = config['email']['inbound']


def periodic_loop(people: Dict[str, person]) -> None:
    phone_numbers = set(list(people))
    seen_emails = set()

    try:
        while True:
            emails: List[MailMessage] = retrieve(
                INBOUND['host'], USERNAME, PASSWORD, phone_numbers)

            for email in emails:
                potential: Tuple[person, str] = marshal_person(email.from_, people)
                if potential:
                    person_, number = potential
                else:
                    # TODO: handle error of unknown person
                    continue

                seen_emails, seen, text = process_email(seen_emails, email)

                print(person_.fname, person_.lname, number, text)

            exit()
            sleep(BACKOFF)
    except KeyboardInterrupt:
        print('Program exit request by user. Exiting.')


if __name__ == '__main__':
    mode = 'Sunday service'  # or Friday large group

    tracked_people: Dict[str, person] = dict()
    for person_ in people:
        next_person = person(person_)
        tracked_people[next_person.phone] = next_person

    periodic_loop(tracked_people)
