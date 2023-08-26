# Example 22-7. Reading venue and speakers returns Record objects

>>> event
<Event 'There *Will* Be Bugs'>
>>> event.venue
<Record serial=1449>
>>> event.venue.name
'Portland 251'
>>> for spkr in event.speakers:
...     print(f'{spkr.serial}: {spkr.name}')
...
3471: Anna Martelli Ravenscroft
5199: Alex Martelli
