from rides.nodes import person
from typing import Dict, List


def optimize(people: Dict[str, person], locations: Dict[Dict[str, int]]):
    drivers: List[person] = list()
    passengers: List[person] = list()

    for person_ in people.values():
        if person_.has_car:
            drivers.append(person_)
        elif person_.needs_ride:
            passengers.append(person_)
