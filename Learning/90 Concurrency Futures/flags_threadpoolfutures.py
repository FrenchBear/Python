# flags_threadpoolfutures.py
# Experimentation on concurrency, parallel version using threadpools, and more details on futures
# From Fluent Python, §17
# 2021-09-04    PV

from concurrent import futures
from flags_sequential import save_flag, get_flag, show, main

def download_one(country):
    image = get_flag(country)
    show(country)
    save_flag(image, country.lower() + '.png')
    return country

def download_many(cc_list):
    cc_list = cc_list[:5]          # Only load the 1st 5 flags
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do = []
        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc)
            to_do.append(future)
            msg = 'Scheduled for {}: {}'
            print(msg.format(cc, future))

        results = []
        for future in futures.as_completed(to_do):
            res = future.result()
            msg = '{} result: {!r}'
            print(msg.format(future, res))
            results.append(res)

    return len(results)

if __name__ == '__main__':
    main(download_many)