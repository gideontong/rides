from random import sample
from rides.nodes import person
from rides.nodes.optimizer import optimize
from rides.sms import send_message
from rides.sms.server import responder
from rides.util import (
    config, locations, domains,
    people
)
from rides.util.log import logger
from typing import Dict


EMAIL = config['email']

USERNAME = EMAIL['username']
PASSWORD = EMAIL['password']

HOST = EMAIL['outbound']['host']
PORT = EMAIL['outbound']['port']
INBOUND = EMAIL['inbound']


def email_next_step(people: Dict[str, person]):
    for person_ in people.values():
        if not (person_.needs_ride or person_.has_car or person_.declined):
            return False
    return True


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

    responder.run(debug=True)

    # test_optimizer(tracked_people)
