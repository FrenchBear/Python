# Example 22-10. Extract from the doctests of schedule_v2.py

>>> event = Record.fetch('event.33950')
>>> event
<Event 'There *Will* Be Bugs'>
>>> event.venue
<Record serial=1449>
>>> event.venue.name
'Portland 251'
>>> event.venue_serial
1449
