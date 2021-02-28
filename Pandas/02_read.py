# Learning Pandas
# 2021-02-27    PV

import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
from pandas.core.reshape import tile
import os, sys
from time import perf_counter

source_folder = r'\\teraz\system\Temp\TestFS Data'
source_file = 'testfs.log'
cache_folder = r'data'
cache_file = source_file.replace('.log', '.feather')

source_file_fp = os.path.join(source_folder, source_file)
cache_file_fp = os.path.join(cache_folder, cache_file)

if not os.path.isdir(source_folder):
    print(f'Subfolder folder "{source_folder}" not found.')
    sys.exit()
if not os.path.isfile(source_file_fp):
    print(f'Source file "{source_file}" not found')
    sys.exit()
if not os.path.isdir(cache_folder):
    print(f'Cache folder "{cache_folder}" not found.')
    sys.exit()

reload_cache = False
if not os.path.isfile(cache_file_fp):
    reload_cache = True
else:
    if os.path.getmtime(source_file_fp)>os.path.getmtime(cache_file_fp):
        reload_cache = True

# pandas file perf
# https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html

if reload_cache:
    print('Building cache, wait for csv loading.')
    headers = ['Date', 'Server', 'tFile', 'tCP', 'tCPU', 'tRAM', 'memPhys', 'usePhys', 'memVirt', 'useVirt', 'sessTot', 'sessAct', 'uptime']
    dtypes = {'Date':'str', 'Server':'str', 'tFile':'float', 'tCP':'float', 'tCPU':'float', 'tRAM':'float', 'memPhys':'float', 'usePhys':'float', 'memVirt':'float', 'useVirt':'float', 'sessTot':'Int32', 'sessAct':'Int32', 'uptime':'float'}
    tstart = perf_counter()
    df = pd.read_csv(source_file_fp, sep='\t', header=None, index_col=False, names=headers, dtype=dtypes, parse_dates=['Date'])
    elapsed_read = perf_counter() - tstart
    tstart = perf_counter()
    print("Saving cache")
    df.to_feather(cache_file_fp)
    elapsed_write = perf_counter() - tstart
    print(f'Done.  Time read={elapsed_read:.3f}, write={elapsed_write:.3f}')
else:
    print('Loading data from cache')
    tstart = perf_counter()
    df = pd.read_feather(cache_file_fp)
    elapsed_read = perf_counter() - tstart
    print(f'Done.  Time read={elapsed_read:.3f}')

"""

df['Date15'] = df['Date'].apply(lambda dt: datetime.datetime(dt.year, dt.month, dt.day, dt.hour,15*(dt.minute // 15)))

#print(df.tail())
#print()
#print(df.info())
#print()
# print(df.shape)
# print()

" ""
res = df.groupby('Server').tFile.agg(['mean'])
print(res)

z = df.groupby('Server')
print(z)
" ""

dg:DataFrame = df.pivot_table(index='Date15', columns='Server', values='tRAM', aggfunc='mean')
print(dg)
dg.plot(title='tRam avg/15 min').legend(loc='center left',bbox_to_anchor=(1.0, 0.5))
plt.show()

#p = plt.plot(dg)
#plt.show()
"""