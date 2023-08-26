# Example 22-2. Interactive exploration of osconfeed.json

>>> import json
>>> with open('data/osconfeed.json') as fp:
...     feed = json.load(fp)
>>> sorted(feed['Schedule'].keys())
['conferences', 'events', 'speakers', 'venues']
>>> for key, value in sorted(feed['Schedule'].items()):
...     print(f'{len(value):3} {key}')
...
  1 conferences
484 events
357 speakers
 53 venues
>>> feed['Schedule']['speakers'][-1]['name']
'Carina C. Zona'
>>> feed['Schedule']['speakers'][-1]['serial']
141590
>>> feed['Schedule']['events'][40]['name']
'There *Will* Be Bugs'
>>> feed['Schedule']['events'][40]['speakers']
[3471, 5199]
