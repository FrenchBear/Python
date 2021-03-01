import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
from pandas.core.reshape import tile
import os, sys
from time import perf_counter

load_csv = True

source_folder = r'\\teraz\system\Temp\TestFS Data'
source_file = 'testfs_small.log'
cache_folder = r'cache'
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

if load_csv:
    print('Loading CSV, please wait.')
    headers = ['Date', 'Server', 'tFile', 'tCP', 'tCPU', 'tRAM', 'memPhys', 'usePhys', 'memVirt', 'useVirt', 'sessTot', 'sessAct', 'uptime']
    dtypes = {'Date':'str', 'Server':'str', 'tFile':'float', 'tCP':'float', 'tCPU':'float', 'tRAM':'float', 'memPhys':'float', 'usePhys':'float', 'memVirt':'float', 'useVirt':'float', 'sessTot':'Int32', 'sessAct':'Int32', 'uptime':'float'}
    tstart = perf_counter()
    df = pd.read_csv(source_file_fp, sep='\t', header=None, index_col=False, names=headers, dtype=dtypes, parse_dates=['Date'])
    elapsed_read = perf_counter() - tstart
    df_bad = df[df.tFile.isnull()]
    if not df_bad.empty:
        print("Invalid lines, stop processing")
        print(df_bad)
        sys.exit()
    tstart = perf_counter()
    print("Saving cache")
    df.to_feather(cache_file_fp)
    elapsed_write = perf_counter() - tstart
    print(f'Done.  Time read={elapsed_read:.3f}, write={elapsed_write:.3f}')
else:
    print('Loading data from cache.')
    tstart = perf_counter()
    df = pd.read_feather(cache_file_fp)
    elapsed_read = perf_counter() - tstart
    print(f'Done.  Time read={elapsed_read:.3f}')


print(df.info())
print()

date_from = np.datetime64('2021-02-18 21:00:00')
dg:DataFrame = df[(df.Server!='EU50TSVP412') & (df.Date>=date_from)]
dg.reset_index(inplace=True, drop=True)
print(dg.info())
print(dg.shape)
