# Weather.py
# Learning Python
# From https://www.hackster.io/gatoninja236/real-time-weather-with-raspberry-pi-4-ad621f
#
# 2019-08-28    PV

import time
import requests
from pprint import pprint

with open(r'C:\Local\openweathermap.txt', encoding='utf_8') as f:
    api_key = f.read()

settings = {
    'api_key':api_key,
    'zip_code':'38000',
    'country_code':'fr',
    'temp_unit':'metric'} #unit can be metric, imperial, or kelvin

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?appid={0}&zip={1},{2}&units={3}"

while True:
    final_url = BASE_URL.format(settings["api_key"],settings["zip_code"],settings["country_code"],settings["temp_unit"])
    weather_data = requests.get(final_url).json()
    pprint(weather_data)
    time.sleep(20) #get new data every 20 seconds
