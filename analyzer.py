from collections import OrderedDict
from pip._vendor.requests.packages.urllib3.packages import ordered_dict

__author__ = 'aoden'
import pandas as pd
from pandas import DataFrame
import matplotlib
import matplotlib.pyplot as plt
matplotlib.matplotlib_fname()
matplotlib.get_backend()
import threading
import numpy as np

df_2008_pollster = pd.read_csv('2008-polls.csv')
df_2012_pollster = pd.read_csv('2012-polls.csv')
df_2008_result = pd.read_csv('2008-results.csv')
df_2012_result = pd.read_csv('2012-results.csv')

df_2008_pollster = DataFrame(df_2008_pollster)
df_2012_pollster = DataFrame(df_2012_pollster)

pollsters_2008 = df_2008_pollster['Pollster'].tolist()
states_2008 = df_2008_pollster['State'].tolist()

# print(df_2008_pollster[(df_2008_pollster.Pollster == 'Rasmussen') & (df_2008_pollster.State == 'AL')])
unique_2008_pollster = pd.unique(df_2008_pollster.Pollster.ravel())
unique_2008_state = pd.unique(df_2008_pollster.State.ravel())
unique_2012_state = pd.unique(df_2012_pollster.State.ravel())
unique_2012_pollster = pd.unique(df_2012_pollster.Pollster.ravel())
# print unique_2008_pollster

dict_pollster_2008 = OrderedDict()
dict_pollster_state_2008 = OrderedDict()
dict_pollster_per_state_2008 = OrderedDict()

dict_pollster_change = OrderedDict()
dict_pollster_per_state_percentage_change = OrderedDict()
dict_pollster_result_est_2008 = OrderedDict()
dict_pollster_result_est_2012 = OrderedDict()

dict_pollster_2012 = OrderedDict()
dict_pollster_state_2012 = OrderedDict()
dict_pollster_per_state_2012 = OrderedDict()

for state in unique_2008_state:
    dict_pollster_per_state_2008[state] = len(pd.unique(df_2008_pollster[df_2008_pollster['State'] == state].Pollster))

for state in unique_2012_state:
    dict_pollster_per_state_2012[state] = len(pd.unique(df_2012_pollster[df_2012_pollster['State'] == state].Pollster))

for state in unique_2008_state:
    default = 0
    original = dict_pollster_per_state_2008[state]
    dict_pollster_per_state_percentage_change[state] = (dict_pollster_per_state_2012.get(state, default) - original) * 100 / original

for state in unique_2012_state:
    dict_pollster_per_state_2012[state] = len(pd.unique(df_2012_pollster[df_2012_pollster['State'] == state].Pollster))

# print dict_pollster_per_state_2008
# print dict_pollster_per_state_2012

for pollster in unique_2008_pollster:
    dict_pollster_2008[pollster] = df_2008_pollster[(df_2008_pollster.Pollster == pollster)]
    dict_pollster_state_2008[pollster] = len(df_2008_pollster[df_2008_pollster['Pollster'] == pollster])
for pollster in unique_2012_pollster:
    dict_pollster_2008[pollster] = df_2012_pollster[(df_2012_pollster.Pollster == pollster)]
    dict_pollster_state_2012[pollster] = len(df_2012_pollster[df_2012_pollster['Pollster'] == pollster])

for pollster in unique_2008_pollster:
    min = 100
    for state in unique_2008_state:
        results_temp = df_2008_pollster[(df_2008_pollster.Pollster == pollster) & (df_2008_pollster.State == state)]
        actual_result_temp = df_2008_result[(df_2008_result.State == state)]
        if not results_temp.empty:
            avg = results_temp.Dem.ravel().mean()
            actual = actual_result_temp.Dem.ravel().mean()
            if (abs(actual - avg) < min):
                min = abs(actual - avg)
                dict_pollster_result_est_2008[state] = pollster

for pollster in unique_2012_pollster:
    min = 100
    for state in unique_2012_state:
        results_temp = df_2012_pollster[(df_2012_pollster.Pollster == pollster) & (df_2012_pollster.State == state)]
        actual_result_temp = df_2012_result[(df_2012_result.State == state)]
        if not results_temp.empty:
            avg = results_temp.Dem.ravel().mean()
            actual = actual_result_temp.Dem.ravel().mean()
            if (abs(actual - avg) < min):
                min = abs(actual - avg)
                dict_pollster_result_est_2012[state] = pollster

print(dict_pollster_result_est_2008)
print(dict_pollster_result_est_2012)
# # average = results_temp.mean()
# dict_pollster_result_est_2008[pollster] = results_temp

for pollster in unique_2012_pollster:
    for state in unique_2012_state:
        results_temp = df_2012_pollster[(df_2008_pollster.Pollster == pollster) & (df_2012_pollster.State == state)]
        # average = sum(results_temp) / float(len(results_temp))
        dict_pollster_result_est_2012[pollster] = results_temp

# print(dict_pollster_result_est_2008)
# print(dict_pollster_result_est_2012)


for pollster in dict_pollster_state_2008:
    default = 0
    original = dict_pollster_state_2008.get(pollster, default)
    change = dict_pollster_state_2008.get(pollster, default) - dict_pollster_state_2012.get(pollster, default)
    dict_pollster_change[pollster] = (change * 100 / original)

for pollster in dict_pollster_state_2012:
    default = 0
    original = dict_pollster_state_2012.get(pollster, default)
    if dict_pollster_state_2012.get(pollster, default) > dict_pollster_state_2008.get(pollster, default):
        change = dict_pollster_state_2012.get(pollster, default) - dict_pollster_state_2008.get(pollster, default)
    else:
        change = dict_pollster_state_2008.get(pollster, default) - dict_pollster_state_2012.get(pollster, default)
    dict_pollster_change[pollster] = (change * 100 / original)

def plot(data_dict, title, ylabel, xlabel):

    width = 0.3
    plt.bar(np.arange(len(data_dict)), data_dict.values(), align='center')
    plt.xticks(np.arange(len(data_dict) + width / 2), data_dict.keys(), rotation=60, size= 1)
    plt.title(title, y=1.08)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.grid(True)
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(18.5, 10.5)
    fig.savefig('test2png.png', dpi=1000)
    plt.show()

# threading.Thread(target= plot(dict_pollster_state_2008, "Pollster occurences " + "2008", "Number of occurences", "Polsters")).start()
# threading.Thread(target= plot(dict_pollster_state_2012, "Pollster occurences " + "2012", "Number occurences", "Pollsters")).start()

# threading.Thread(target= plot(dict_pollster_change, "Pollster occurences" + " change", "Changes", "Pollsters")).start()
# threading.Thread(target= plot(dict_pollster_per_state_percentage_change, "Pollster number per state " + " change", "Changes(%)", "Pollsters")).start()

# threading.Thread(target= plot(dict_pollster_per_state_2008, "Number of pollster per state " + "2008", "Number of pollster", "States")).start()
# threading.Thread(target= plot(dict_pollster_per_state_2012, "Number of pollster per state " + "2012", "Number of pollster", "States")).start()

# print(dict_pollster_state_2008)
# print(dict_pollster_state_2012)

# print pd.unique(df_2012_pollster.Pollster.ravel())
