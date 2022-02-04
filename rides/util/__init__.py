from json import load
from typing import Tuple, Union


with open('config/keys.json') as fp:
    config = load(fp)

with open('config/domains.json') as fp:
    domains = load(fp)

with open('config/people.json') as fp:
    people = load(fp)


def marshal_person(address: str, people: dict) -> Union[Tuple[str, str], None]:
    username = address.split('@')[0]

    for person in people:
        if username in address:
            return person, people[person].number
    
    return None
