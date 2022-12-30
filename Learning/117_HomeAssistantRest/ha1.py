# Home Assistant Rest Interface
# 2022-12-30    PV
#
# https://developers.home-assistant.io/docs/api/rest/

import requests
import json
from typing import Tuple

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhMDc5NDA4YWMwY2M0MjllOTkyYTkwOWUxOTVkNjRlNyIsImlhdCI6MTY3MjQzMTMxNCwiZXhwIjoxOTg3NzkxMzE0fQ.l8LxNUfnZzCzTIfjO1gxsFULAqurQJ-UzjMi6FjMdPE",
    "content-type": "application/json",
}


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
    return (data['state'], data['attributes']['unit_of_measurement'], data['attributes']['friendly_name'])


temp = get_state('sensor.th_1_ch_b_temperature')
print(temp)


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


res = call_service('light', 'toggle', 'light.amp_ikea_ws_1056lm_1_plafond_bureau_pierre')
print(res)
