from csv import DictReader
from json import dump


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
