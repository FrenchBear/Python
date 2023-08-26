# Example 22-3. FrozenJSON from Example 22-4 allows reading attributes like name, and calling methods like .keys() and .items()

>>> import json
>>> raw_feed = json.load(open('data/osconfeed.json'))
>>> feed = FrozenJSON(raw_feed)
>>> len(feed.Schedule.speakers)
357
>>> feed.keys()
dict_keys(['Schedule'])
>>> sorted(feed.Schedule.keys())
['conferences', 'events', 'speakers', 'venues']
>>> for key, value in sorted(feed.Schedule.items()):
...     print(f'{len(value):3} {key}')
...
  1 conferences
484 events
357 speakers
 53 venues
>>> feed.Schedule.speakers[-1].name
'Carina C. Zona'
>>> talk = feed.Schedule.events[40]
>>> type(talk)
<class 'explore0.FrozenJSON'>
>>> talk.name
'There *Will* Be Bugs'
>>> talk.speakers
[3471, 5199]
>>> talk.flavor
Traceback (most recent call last):
  ...
KeyError: 'flavor'
