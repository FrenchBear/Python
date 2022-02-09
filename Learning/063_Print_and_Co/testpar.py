# testpar.py
# Leaning python, variations on parallel print
# From "Your Guide to the Python Print Function", https://realpython.com/python-print/
#
# 2019-08-29    PV

import sys
from time import sleep
from random import random
from threading import current_thread, Thread, Lock
from unittest.mock import patch
import logging

logging.basicConfig(format='%(threadName)s %(message)s')

write = sys.stdout.write

def slow_write(text):
    sleep(random())
    write(text)

lock = Lock()
def thread_safe_print(*args, **kwargs):
    with lock:
        logging.error('Lock acquired')
        print(*args, **kwargs)
        logging.error('Lock released')

def task():
    thread_name = current_thread().name
    for letter in 'ABC':
        #print(f'[{thread_name} {letter}]\n', end='')
        thread_safe_print(f'[{thread_name} {letter}]')

with patch('sys.stdout') as mock_stdout:
    mock_stdout.write = slow_write
    for _ in range(3):
        Thread(target=task).start()
