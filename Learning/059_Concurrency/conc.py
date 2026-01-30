# 59 conc.py
# Learning Python - Concurrency
# From https://realpython.com/python-concurrency/
#
# 2019-01-15	PV

# -------------------------------------------------
# Synchronous version

import aiohttp
import multiprocessing
import asyncio
import threading
import requests
import concurrent.futures
import time


def download_site_synchronous(url, session):
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")


def download_all_sites_synchronous(sites: list[str]):
    with requests.Session() as session:
        for url in sites:
            download_site_synchronous(url, session)


def test_synchronous():
    sites = [
        "http://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 20
    start_time = time.time()
    download_all_sites_synchronous(sites)
    duration = time.time() - start_time
    print(f"synchronous: Downloaded {len(sites)} in {duration} seconds")


# -------------------------------------------------
# threading version


thread_local = threading.local()


def get_session_for_thread():
    if not getattr(thread_local, "session", None):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site_threading(url):
    session = get_session_for_thread()
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")


def download_all_sites_threading(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_site_threading, sites)


def test_threading():
    sites = [
        "http://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 20
    start_time = time.time()
    download_all_sites_threading(sites)
    duration = time.time() - start_time
    print(f"threading: Downloaded {len(sites)} in {duration} seconds")


# -------------------------------------------------
# asyncio version


async def download_site_asyncio(session, url):
    async with session.get(url) as response:
        print(f"Read {response.content_length} from {url}")


async def download_all_sites_asyncio(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.ensure_future(download_site_asyncio(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


def test_asyncio():
    sites = [
        "http://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 20
    start_time = time.time()
    # asyncio.get_event_loop().run_until_complete(download_all_sites(sites))
    asyncio.run(download_all_sites_asyncio(sites))       # Same as previous line in Python 3.7
    duration = time.time() - start_time
    print(f"asyncio: Downloaded {len(sites)} sites in {duration} seconds")


# -------------------------------------------------
# multiprocessing


session = None


def set_global_session():
    global session
    if not session:
        session = requests.Session()


def download_site_multiprocessing(url):
    with session.get(url) as response:
        name = multiprocessing.current_process().name
        print(f"{name}:Read {len(response.content)} from {url}")


def download_all_sites_multiprocessing(sites):
    with multiprocessing.Pool(initializer=set_global_session) as pool:
        pool.map(download_site_multiprocessing, sites)


def test_multiprocessing():
    sites = [
        "http://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 20
    start_time = time.time()
    download_all_sites_multiprocessing(sites)
    duration = time.time() - start_time
    print(f"multiprocessing: Downloaded {len(sites)} in {duration} seconds")


# -------------------------------------------------
# Main
if __name__ == '__main__':
    # multiprocessing.freeze_support()
    # test_synchronous()
    # test_threading()
    # test_asyncio()
    test_multiprocessing()
