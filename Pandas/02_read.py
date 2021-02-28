# Learning Pandas
# 2021-02-27    PV

import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
from pandas.core.reshape import tile

# headers = ['Date', 'Server', 'tFile', 'tCP', 'tCPU', 'tRAM', 'memPhys', 'usePhys', 'memVirt', 'useVirt', 'sessTot', 'sessAct', 'uptime']
# dtypes = {'Date':'str', 'Server':'str', 'tFile':'float', 'tCP':'float', 'tCPU':'float', 'tRAM':'float', 'memPhys':'float', 'usePhys':'float', 'memVirt':'float', 'useVirt':'float', 'sessTot':'Int32', 'sessAct':'Int32', 'uptime':'float'}
# print("loading")
# df = pd.read_csv(r'smalltestfs.log', sep='\t', header=None, index_col=False, names=headers, dtype=dtypes, parse_dates=['Date'])
# print("saving")
# df.to_feather("example.feather")
# print("done")
df = pd.read_feather("example.feather")



df['Date15'] = df['Date'].apply(lambda dt: datetime.datetime(dt.year, dt.month, dt.day, dt.hour,15*(dt.minute // 15)))

#print(df.tail())
#print()
#print(df.info())
#print()
# print(df.shape)
# print()

"""
res = df.groupby('Server').tFile.agg(['mean'])
print(res)

z = df.groupby('Server')
print(z)
"""

dg:DataFrame = df.pivot_table(index='Date15', columns='Server', values='tRAM', aggfunc='mean')
print(dg)
dg.plot(title='tRam avg/15 min').legend(loc='center left',bbox_to_anchor=(1.0, 0.5))
plt.show()

#p = plt.plot(dg)
#plt.show()
