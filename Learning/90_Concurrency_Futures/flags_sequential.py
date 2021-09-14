# flags_sequential.py
# Experimentation on concurrency, non-parallel version
# From Fluent Python, §17
# 2021-09-04    PV

import os
import platform
import time
import sys

import requests

POP20_CC = 'france italy spain china india brazil russia japan egypt portugal germany england canada argentina ukraine algeria peru yemen ecuador cuba'.split()
BASE_URL = 'https://cdn.countryflags.com/thumbs/{country}/flag-square-500.png'

if (pl := platform.system()) == 'Windows':
    DEST_DIR = r'C:\Downloads'
elif pl == 'Linux':
    DEST_DIR = '/home/pierre/downloads'
elif pl == 'Darwin':
    DEST_DIR = 'Users/pierre/Downloads'
else:
    DEST_DIR = '.'
DEST_DIR = os.path.join(DEST_DIR, 'Flags')
if not os.path.exists(DEST_DIR):
    try:
        os.mkdir(DEST_DIR)
    except Exception as ex:
        print(f'*** Error creating folder {DEST_DIR}: {ex}')
        sys.exit(1)


def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


def get_flag(country):
    url = BASE_URL.format(country=country)
    resp = requests.get(url)
    return resp.content


def show(text):
    print(text, end=' ')
    sys.stdout.flush()


def download_many(country_list):
    for country in sorted(country_list):
        image = get_flag(country)
        show(country)
        save_flag(image, country.lower() + '.png')
    return len(country_list)


def main(download_many):
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main(download_many)
