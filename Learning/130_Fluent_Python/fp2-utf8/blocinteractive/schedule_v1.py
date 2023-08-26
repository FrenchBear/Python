# Example 22-8. Test-driving schedule_v1.py (from Example 22-9)

>>> records = load(JSON_PATH)
>>> speaker = records['speaker.3471']
>>> speaker
<Record serial=3471>
>>> speaker.name, speaker.twitter
('Anna Martelli Ravenscroft', 'annaraven')
