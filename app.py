from datetime import datetime
from imap_tools import MailMessage
from pytz import UTC
from random import sample
from rides.email.sender import send
from rides.email.receiver import retrieve
from rides.nodes import person
from rides.nodes.optimizer import optimize
from rides.util import (
    config, locations, domains,
    people, marshal_person
)
from rides.util.email import process_email
from rides.util.log import logger
from time import sleep
from typing import Dict, List, Tuple


BACKOFF = 10

EMAIL = config['email']
USERNAME = EMAIL['username']
PASSWORD = EMAIL['password']

HOST = EMAIL['outbound']['host']
PORT = EMAIL['outbound']['port']

INBOUND = config['email']['inbound']


def ready_next_step(people: Dict[str, person]):
    for person_ in people.values():
        if not (person_.needs_ride or person_.has_car or person_.declined):
            return False
    return True


def periodic_loop(people: Dict[str, person], mode: str) -> None:
    start_time = datetime.utcnow().replace(tzinfo=UTC)
    print(f'Waiting {BACKOFF} seconds to allow timestamp offset')
    sleep(BACKOFF)

    phone_numbers = set(list(people))
    seen_emails = set()

    for number in people:
        subject, body = people[number].wrap_next_step(mode)
        send(HOST, PORT, USERNAME, PASSWORD,
             people[number].email(), subject, body)

    try:
        while True:
            logger.info('Retrieving new messages from the server')
            emails: List[MailMessage] = retrieve(
                INBOUND['host'], USERNAME, PASSWORD, phone_numbers)

            logger.debug(f'Processing {len(emails)} emails from the server')
            for email in emails:
                potential: Tuple[person, str] = marshal_person(
                    email.from_, people)
                if potential:
                    person_, number = potential
                else:
                    # TODO: handle error of unknown person
                    continue

                seen_emails, seen, text = process_email(seen_emails, email)

                if not seen and email.date > start_time:
                    logger.info(f'Processing new text from {person_.fname}: {" ".join(text.split())}')
                    subject, body = person_.wrap_next_step(mode, text)
                    send(HOST, PORT, USERNAME, PASSWORD,
                         person_.email(), subject, body)

            print(f'Waiting {BACKOFF} seconds')
            sleep(BACKOFF)
    except KeyboardInterrupt:
        logger.warning('User requested exit, exiting now')


def test_optimizer(people: Dict[str, person]):
    # Randomly assign drivers and passengers
    driver_count = len(people) // 5 + 1
    drivers = set(sample(list(people), driver_count))
    for driver_key in drivers:
        people[driver_key].has_car = True
        people[driver_key].passengers = 4

    for passenger_key in set(people) - drivers:
        people[passenger_key].needs_ride = True

    # Run passenger assignment
    optimize(people, locations)


if __name__ == '__main__':
    logger.info('Welcome to Kairos Rides Organizer')
    mode = 'Sunday service'  # or Friday large group

    logger.debug('Importing people from database to memory')
    tracked_people: Dict[str, person] = dict()
    for person_ in people:
        next_person = person(person_)
        tracked_people[next_person.phone] = next_person
    logger.debug(f'{len(tracked_people)} people now being processed in memory')

    test_optimizer(tracked_people)
    # periodic_loop(tracked_people, mode)
