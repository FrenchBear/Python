# Example 20-9. Sample run of demo_executor_map.py from Example 20-8

>>> import time
>>> from tqdm import tqdm
>>> for i in tqdm(range(1000)):
...     time.sleep(.01)
...
>>> # -> progress bar will appear here <-
