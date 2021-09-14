# flags_threadpool.py
# Experimentation on concurrency, parallel version using threadpools
# From Fluent Python, §17
# 2021-09-04    PV

from concurrent import futures
from flags_sequential import save_flag, get_flag, show, main

MAX_WORKERS = 20

def download_one(country):
    image = get_flag(country)
    show(country)
    save_flag(image, country.lower() + '.png')
    return country

def download_many(country_list):
    workers = min(MAX_WORKERS, len(country_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one, sorted(country_list))
    return len(list(res))

if __name__ == '__main__':
    main(download_many)