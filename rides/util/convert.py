from csv import DictReader
from json import dump


def people_from_csv(infile: str, outfile: str) -> None:
    with open(infile, encoding='utf-8') as fp:
        reader = DictReader(fp)

        people = list()
        for row in reader:
            people.append({
                'fname': row['First Name'],
                'lname': row['Last Name'],
                'phone': row['Phone Number'],
                'carrier': row['Mobile Carrier'],
                'address': row['Address']
            })
    
    with open(outfile, 'w', encoding='utf-8') as fp:
        dump(people, fp, indent=4, sort_keys=True)


def address_from_csv(infile: str, outfile: str) -> None:
    addresses = dict()
    with open(infile) as fp:
        reader = DictReader(fp)
    
        for row in reader:
            src = row['Src']
            dest = row['Dest']

            if src not in addresses:
                addresses[src] = {
                    src: {
                        'dist': 0,
                        'time': 0
                    }
                }
            
            if dest not in addresses:
                addresses[dest] = {
                    dest: {
                        'dist': 0,
                        'time': 0
                    }
                }
            
            if dest not in addresses[src]:
                addresses[src][dest] = {
                    'dist': int(row['FrozenDist']),
                    'time': int(row['FrozenTime'])
                }
            
            if src not in addresses[dest]:
                addresses[dest][src] = {
                    'dist': int(row['FrozenDist']),
                    'time': int(row['FrozenTime'])
                }
    
    with open(outfile, 'w') as fp:
        dump(addresses, fp, sort_keys=True, indent=4)
