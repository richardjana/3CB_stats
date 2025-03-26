import numpy as np
import pandas as pd
from analysis import load_data

import matplotlib.pyplot as plt

data = load_data()
player = 'hug77'

### versoin 1: boxplots with player on top ###
'''
boxes = data.groupby('round')['%'].apply(list)
perc = data.loc[data['player']==player][['round', '%']].to_numpy()
fig, ax = plt.subplots()
ax.boxplot(boxes, notch=True, boxprops=dict(alpha=.3)) # just clutters everything
ax.plot(perc[:,0], perc[:,1]) # sort first
plt.show()
'''

### version 2: lines for all players, other players grey ###
lines = data.groupby('player')[['round', '%']]
fig, ax = plt.subplots()
for p, a in lines:
    a = a.to_numpy()
    a = a[a[:, 0].argsort()]
    #if p == player:
    #    ax.plot(a[:,0], a[:,1], c='k', linewidth=2)
    #else:
    ax.plot(a[:,0], a[:,1], c='grey')
perc = data.loc[data['player']==player][['round', '%']].to_numpy()
perc = perc[perc[:, 0].argsort()]
ax.plot(perc[:,0], perc[:,1], c='k', linewidth=2)
plt.show()
