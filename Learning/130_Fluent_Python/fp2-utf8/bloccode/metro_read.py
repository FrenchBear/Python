# Example 28-3. metro_read.py: list all records from metro_areas.bin

from struct import iter_unpack

FORMAT = 'i12s2sf'

def text(field: bytes) -> str:
    octets = field.split(b'\0', 1)[0]
    return octets.decode('cp437')

with open('metro_areas.bin', 'rb') as fp:
    data = fp.read()

for fields in iter_unpack(FORMAT, data):
    year, name, country, pop = fields
    place = text(name) + ', ' + text(country)
    print(f'{year}\t{place}\t{pop:,.0f}')
