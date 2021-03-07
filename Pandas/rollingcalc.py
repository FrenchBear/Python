# RunningCalc.py
# Lerning to do ruinning calculations (ex: moving average) on rows values
# 2021-03-07    PV

import datetime
import os
import sys
from time import perf_counter
from enum import Enum
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
import random

# Build a random dataframe
"""
datebase = datetime.datetime(2021, 1, 1)
daterange = [datebase+datetime.timedelta(days=i) for i in range(31)]
values = [random.random()for i in range(31)]
df = DataFrame({'Data': values}, index=daterange)
"""

df = pd.DataFrame(1+np.random.random(31)*0.2,
                  index=pd.date_range('2021-01-01', periods=31),
                  columns=['Data'])
df['Data'][15:32] *= 2


def S4(x):
    # X is a series of 4 values, cal be accessed using x[0]..x[3]
    # return x[0]+x[1]+x[2]+x[3]
    sd = x[1:4].std()
    av = x[1:4].mean()
    return 1 if abs(x[0]-av) > 4*sd else 0


# df['M4'] = df.rolling(4, min_periods=4).mean()

df['S4'] = df['Data'].rolling(4, min_periods=4).apply(S4)


fig = plt.figure(figsize=(2, 2))
fig.subplots_adjust(left=0.065, bottom=0.05, right=0.975, top=0.95)
fig.canvas.manager.window.state('zoomed')

ax: Axes = fig.add_subplot(2, 2, 1)
ax.set_title('Raw data')
lines1 = ax.plot(df)
#ax.set_xticks(daterange, minor=False)
ax.grid()
plt.xticks(rotation=90)
legend = ax.legend(df.columns, loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize='x-small')

plt.show()
