__author__ = 'aoden'
import pandas as pd
from pandas import DataFrame
import matplotlib
import matplotlib.pyplot as plt
matplotlib.matplotlib_fname()
matplotlib.get_backend()

df_2008_pollster = pd.read_csv('2008-polls.csv')
df_2012_pollster = pd.read_csv('2012-polls.csv')

df_2008_pollster = DataFrame(df_2008_pollster)
df_2012_pollster = DataFrame(df_2012_pollster)

pollsters_2008 = df_2008_pollster['Pollster'].tolist()
states_2008 = df_2008_pollster['State'].tolist()

# print(df_2008_pollster[(df_2008_pollster.Pollster == 'Rasmussen') & (df_2008_pollster.State == 'AL')])
unique_2008_pollster = pd.unique(df_2008_pollster.Pollster.ravel())
unique_2012_pollster = pd.unique(df_2012_pollster.Pollster.ravel())
# print unique_2008_pollster

dict_pollster_2008 = dict()
dict_pollster_state_2008 = dict()

dict_pollster_2012 = dict()
dict_pollster_state_2012 = dict()

for pollster in unique_2008_pollster:
    dict_pollster_2008[pollster] = df_2008_pollster[(df_2008_pollster.Pollster == pollster)]
    dict_pollster_state_2008[pollster] = len(df_2008_pollster[df_2008_pollster['Pollster'] == pollster])
for pollster in unique_2012_pollster:
    dict_pollster_2008[pollster] = df_2012_pollster[(df_2012_pollster.Pollster == pollster)]
    dict_pollster_state_2012[pollster] = len(df_2012_pollster[df_2012_pollster['Pollster'] == pollster])

plt.bar(range(len(dict_pollster_state_2008)), dict_pollster_state_2008.values(), align='center')
plt.xticks(range(len(dict_pollster_state_2008)), dict_pollster_state_2008.keys())
plt.show()

print(dict_pollster_state_2008)
print(dict_pollster_state_2012)

# print pd.unique(df_2012_pollster.Pollster.ravel())
