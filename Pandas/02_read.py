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

force_rebuild_cache = False

source_folder = r'\\teraz\system\Temp\TestFS Data'
source_file = 'testfs.log'
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

reload_cache = force_rebuild_cache
if not reload_cache:
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

df = df[df.Server!='EU50TSVP411']   # 411 does not exist anymore
# DateG is Date column rounded at 15min
df['DateG'] = df['Date'].apply(lambda dt: datetime.datetime(dt.year, dt.month, dt.day, dt.hour,15*(dt.minute // 15)))
#print(df.info())
#print()


import matplotlib.gridspec as gridspec

plt.figure(figsize = (2,2))
# gs1 = gridspec.GridSpec(2, 2)
# gs1.update(wspace=0.025, hspace=0.05) # set the spacing between axes.
plt.subplots_adjust(left=0.065, bottom=0.05, right=0.975, top=0.95)


# uptime
plt.subplot(2,2,1)
plt.title('uptime (days) avg/15 min')
df_uptime:DataFrame = df[df.uptime.notnull() & df.Server!='EU50TSVP411']     # Only take records with values
dp_uptime:DataFrame = df_uptime.pivot_table(index='DateG', columns='Server', values='uptime', aggfunc='mean')
plt.plot(dp_uptime)
plt.legend(dp_uptime.columns, loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize='x-small')
#print(dp_uptime.columns)

# tFile
plt.subplot(2,2,2)
plt.title('tFile (s) avg/15 min')
df_tfile:DataFrame = df[df.tFile.notnull() & (df.Server!='EU50TSVP411')]     # Only take records with values
dp_tfile:DataFrame = df_tfile.pivot_table(index='DateG', columns='Server', values='tFile', aggfunc='mean')
plt.ylim([0.0, 1.0])
plt.plot(dp_tfile)
#plt.legend(dp_tfile.columns, loc='center left', bbox_to_anchor=(1.0, 0.5))
# print(dp_tfile.columns)

# s1 = set(dp_uptime.columns)
# s2 = set(dp_tfile.columns)
# s3 = s2-s1
# print(s3)

# RAM
ax = plt.subplot(2,2,3)
df_ram:DataFrame = df[df.tRAM.notnull() & df.tRAM>0]     # Only take records with values
dp_ram:DataFrame = df_ram.pivot_table(index='DateG', columns='Server', values='tRAM', aggfunc='mean')
#dp_ram.plot(title='tRam avg/15 min').legend(loc='center left',bbox_to_anchor=(1.0, 0.5))
ax.set_xlim([0,10])
ax.set_xticks( np.arange(0,11), minor=False)
dp_ram.boxplot(vert=False, sym='.')
ax.set_title('tRAM boxplot')
ax.set_ylabel('Server')
ax.set_xlabel('tRAM (s)')
#plt.xticks(rotation=90)

# CPU
ax = plt.subplot(2,2,4)
df_cpu:DataFrame = df[df.tCPU.notnull()]     # Only take records with values
dp_cpu:DataFrame = df_cpu.pivot_table(index='DateG', columns='Server', values='tCPU', aggfunc='mean')
#dp_cpu.plot(title='tRam avg/15 min').legend(loc='center left',bbox_to_anchor=(1.0, 0.5))
dp_cpu.boxplot(vert=False, sym='.')
plt.title('tCPU boxplot')
plt.ylabel('Server')
plt.xlabel('tCPU (s)')


plt.get_current_fig_manager().window.state('zoomed')
plt.show()
