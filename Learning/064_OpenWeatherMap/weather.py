# Weather.py
# Learning Python
# From https://www.hackster.io/gatoninja236/real-time-weather-with-raspberry-pi-4-ad621f
#
# 2019-08-28    PV
# 2024-04-30    PV      Subscribed to OpenWeather OneCall API 3.0 to replace 2.5 API, free up to 1000 calls/day

import time
import requests
from pprint import pprint

with open(r'C:\Utils\Local\openweathermap.txt', encoding='utf_8') as f:
    api_key = f.read()

# settings25 = {
#     'api_key':api_key,
#     'zip_code':'38000',
#     'country_code':'fr',
#     'temp_unit':'metric'} #unit can be metric, imperial, or kelvin

# Saint-ismier, 168 allée de la bâtie
lat = '45.238272'
lon = '5.8512146'

# Discontinued end of June 2024
# BASE_URL_25 = "http://api.openweathermap.org/data/3.0/weather?appid={0}&zip={1},{2}&units={3}"

# https://openweathermap.org/api/one-call-3
BASE_URL_30 = "http://api.openweathermap.org/data/3.0/onecall?appid={0}&lat={1}&lon={2}&units=metric&exclude=alerts,daily,minutely,hourly"

while True:
    # final_url = BASE_URL_25.format(settings25["api_key"],settings25["zip_code"],settings25["country_code"],settings25["temp_unit"])
    final_url = BASE_URL_30.format(api_key, lat, lon)
    weather_data = requests.get(final_url).json()
    pprint(weather_data)
    time.sleep(20)  # get new data every 20 seconds
