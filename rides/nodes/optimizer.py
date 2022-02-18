from hashlib import new
from random import choice
from rides.nodes import person
from rides.util.log import logger
from typing import (
    Dict, List, Set,
    Tuple
)


def generate_distance_matrix(driver: person, passengers: List[person], locations: Dict[str, Dict[str, Dict[str, int]]]) -> List[Tuple[person, int]]:
    '''Returns sorted list of (person, distance) to driver'''
    distances: List[Tuple[person, int]] = list()
    for passenger in passengers:
        distances.append((passenger, locations[driver.address][passenger.address]['dist']))
    
    distances.sort(key=lambda v: v[1])
    return distances


def assign_passengers(assigned_drivers: Set[str], drivers: Dict[str, person], passengers: List[person], locations: Dict[str, Dict[str, Dict[str, int]]]) -> Tuple[Set[str], person, List[person], List[person]]:
    assigned_passengers: List[person] = list()
    drivers_left = list(set(drivers) - assigned_drivers)

    # TODO: If there are no drivers left
    if not drivers_left:
        logger.error('Ran out of drivers to assign passengers!')

    driver_key = choice(drivers_left)
    driver = drivers[driver_key]
    logger.debug(f'Chose {driver.fname} as the next driver')

    distances = generate_distance_matrix(driver, passengers, locations)
    while len(passengers) > 0 and len(assigned_passengers) <= driver.passengers:
        passenger, distance = distances.pop(0)
        logger.debug(f'Chose {passenger.fname} with distance {distance} to driver {driver.fname}')
        assigned_passengers.append(passenger)
        passengers.remove(passenger)

    assigned_drivers.add(driver_key)
    return assigned_drivers, driver, assigned_passengers, passengers


def optimize(people: Dict[str, person], locations: Dict[str, Dict[str, Dict[str, int]]]):
    logger.info(f'Now optimizing {len(people)} people with {len(locations)} locations')
    assigned_drivers: Set[str] = set()
    drivers: Dict[str, person] = dict()
    assigned_passengers: Dict[str, List[person]] = dict()
    passengers: List[person] = list()

    for person_ in people.values():
        if person_.has_car:
            drivers[person_.phone] = person_
        elif person_.needs_ride:
            passengers.append(person_)

    total_spots = 0
    for driver in drivers.values():
        total_spots += driver.passengers

    # TODO: If there aren't enough rides
    if len(passengers) > total_spots:
        logger.warning('Not enough spots for all passengers!')

    drivers_left = len(drivers)
    while len(passengers) > 0 or drivers_left > 0:
        logger.debug(f'Assigning drivers and passengers, {len(passengers)} remaining')
        if len(passengers) == 0:
            # TODO: Notify a driver they don't have to drive
            logger.debug('Extra drivers detected, moving some to passengers')
            new_passenger = choice(list(set(drivers) - assigned_drivers))
            if drivers_left > 1:
                logger.debug(f'Converting {drivers[new_passenger].fname} from driver to passenger')
                passengers.append(drivers[new_passenger])
                del drivers[new_passenger]
            else:
                logger.debug(f'A driver remained, which was {drivers[new_passenger].fname}')
                # TODO: Notify a driver they can drive themselves

        assigned_drivers, driver, used_passengers, passengers = assign_passengers(
            assigned_drivers, drivers, passengers, locations)
        assigned_passengers[driver.phone] = used_passengers
        drivers_left = len(drivers) - len(assigned_drivers)
