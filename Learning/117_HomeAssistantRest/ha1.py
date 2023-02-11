# Home Assistant Rest Interface
# 2022-12-30    PV
#
# https://developers.home-assistant.io/docs/api/rest/

import requests
import json
from typing import Tuple

with open(r'C:\Utils\Local\homeassistant.txt', encoding='utf_8') as f:
    api_token = f.read()

headers = {
    "Authorization": "Bearer "+api_token,
    "content-type": "application/json",
}

def beautify_num(value: Tuple[str | None, str | None, str], fmt: str) -> str:
    if value[0]==None:
        return ''
    try:
        val = float(value[0])
        return format(val, fmt) + (' '+value[1] if value[1] and len(value[1])>0 else '')
    except ValueError:
        return value[0]


def get_state(entity: str) -> Tuple[str | None, str | None, str]:
    url = "http://on2ha:8123/api/states/" + entity
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            msg = f'GET returned status {response.status_code}'
            print(msg)
            return (None, None, msg)
    except Exception as ex:
        msg = 'GET error: ' + str(ex)
        print(msg)
        return (None, None, msg)

    data = json.loads(response.text)
    attributes = data['attributes']
    unit = attributes['unit_of_measurement'] if 'unit_of_measurement' in attributes else '' 
    return (data['state'], unit, attributes['friendly_name'])

temp = get_state('sensor.th_1_ch_b_temperature')
print('Temp ch Pierre:', beautify_num(temp, '.1f'))

VA = get_state('sensor.linky_PAPP')
print('Puissance Linky:', beautify_num(VA, '.0f'))

lp = get_state('light.amp_ikea_ws_1056lm_1_plafond_bureau_pierre')
print('Lampe Plafond bureau Pierre:', lp[0])



# Toggle plafond bureau pierre
def call_service(domain: str, service: str, entity_id: str) -> bool:
    url = f"http://on2ha:8123/api/services/{domain}/{service}"
    data = json.loads(f'{{ "entity_id": "{entity_id}" }}')

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 200:
            print(f'POST returned status {response.status_code}')
            return False
    except Exception as ex:
        print('POST error: ' + str(ex))
        return False

    return True


# res = call_service('light', 'toggle', 'light.amp_ikea_ws_1056lm_1_plafond_bureau_pierre')
# print(res)
