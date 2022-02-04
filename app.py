from datetime import datetime
from imap_tools import MailMessage
from pytz import UTC
from rides.email.sender import send
from rides.email.receiver import retrieve
from rides.nodes import person
from rides.util import (
    config, domains, people,
    marshal_person
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


def periodic_loop(people: Dict[str, person], mode: str) -> None:
    start_time = datetime.utcnow().replace(tzinfo=UTC)
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

            sleep(BACKOFF)
    except KeyboardInterrupt:
        logger.warn('User requested exit, exiting now')


if __name__ == '__main__':
    logger.info('Welcome to Kairos Rides Organizer')
    mode = 'Sunday service'  # or Friday large group

    logger.debug('Importing people from database to memory')
    tracked_people: Dict[str, person] = dict()
    for person_ in people:
        next_person = person(person_)
        tracked_people[next_person.phone] = next_person
    logger.debug(f'{len(tracked_people)} people now being processed in memory')

    periodic_loop(tracked_people, mode)
