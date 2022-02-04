from json import load

with open('config/keys.json') as fp:
    config = load(fp)

with open('config/domains.json') as fp:
    domains = load(fp)

with open('config/people.json') as fp:
    people = load(fp)
