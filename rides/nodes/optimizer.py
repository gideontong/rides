from rides.nodes import person
from rides.util.log import logger
from typing import (
    Dict, List, Set,
    Tuple
)


def assign_passengers(assigned_drivers: Set[str], drivers: Dict[str, person], passengers: List[person], locations: Dict[Dict[str, int]]) -> Tuple[Set[str], List[person], List[person]]:
    assigned_passengers: List[person] = list()
    return assigned_drivers, assigned_passengers, passengers


def optimize(people: Dict[str, person], locations: Dict[Dict[str, int]]):
    logger.info(f'Now optimizing {len(people)} people with {len(locations)} locations')
    assigned_drivers: Set[str] = set()
    drivers: Dict[str, person] = list()
    assigned_passengers: Dict[str, person] = list()
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
        pass

    while len(passengers) > 0:
        assigned_drivers, used_passengers, passengers = assign_passengers(
            assigned_drivers, drivers, passengers, locations)
        assigned_passengers += used_passengers
