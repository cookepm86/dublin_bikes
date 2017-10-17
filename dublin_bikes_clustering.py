import json

import seaborn as sns
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

from sklearn.cluster import KMeans

# import datetime

# from scipy import optimize
# from scipy.stats import pearsonr

# import random

# ------------------------------------------------------------------------------

with open('merged_data', 'r') as infile:
    data_dict = json.load(infile)

# ------------------------------------------------------------------------------

day_type = 'weekend'
day = 'sat'
date = '20171014'

data = [x for x in data_dict[day_type][day] if x[0] == date]

# ------------------------------------------------------------------------------

# store lists of the longitudes and latitudes of stations
long_list, lat_list = [], []
length = len(data[0][2])
for n in range(length):
    # define list of longitudes and latitudes of stations
    long_list.append(data[0][2][n]['position']['lng'])
    lat_list.append(data[0][2][n]['position']['lat'])

# ------------------------------------------------------------------------------

sns.set_style(style='darkgrid')
# scatter plot of locations
plt.scatter(long_list, lat_list)

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Geographical locations of Dublin Bikes stations')

plt.show()

# ------------------------------------------------------------------------------

# display on a map
# center plot
# gmap = gmplot.GoogleMapPlotter(53.345, -6.276, 14)
# for some reason can't get scatter to work
# gmap.heatmap(lat_list, long_list)
# draw map
# gmap.draw("dublin_bikes_map.html")

# define an array of longitudes and latitudes
X = np.array([x for x in zip(long_list, lat_list)])

kmeans = KMeans(n_clusters=8, random_state=42).fit(X)

# ------------------------------------------------------------------------------

# plot with labels
cm = plt.cm.get_cmap('RdYlBu')
plt.scatter(long_list, lat_list, c=kmeans.labels_, cmap=cm, edgecolors='black')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Geographical locations of Dublin Bikes stations (clustered)')
plt.show()

# ------------------------------------------------------------------------------

# generate dictionary with list of the bikes available
# ordered by time
bike_dict = {}
for n in range(length):
    bike_list = []
    for time_no in range(len(data)):
        bike_list.append(data[time_no][2][n]['available_bikes'])
    station_name = data[0][2][n]['address']
    bike_dict[station_name] = bike_list

# generate a list of the timestamps
time_stamp_list = []
for time in range(len(data)):
    time_stamp_list.append(data[time][1])

# ------------------------------------------------------------------------------

# plot # available bikes for my station
# plt.plot(bike_dict['Royal Hospital'], 'o')

# plt.xticks(np.arange(0, len(time_stamp_list), 5), time_stamp_list[::5],
#                                                    rotation=45)
# plt.xlabel('time')
# plt.ylabel('# bikes')

# plt.show()

# ------------------------------------------------------------------------------

# store available bike data as a list
bike_station_list = [bike_dict[station] for station in bike_dict.keys()]
# generate dataframe from this list
bike_station_df = pd.DataFrame([x for x in zip(*bike_station_list)])
# transpose the dataframe to get timeseries as rows
bike_station_df = bike_station_df.transpose()
bike_station_df.index = bike_dict.keys() # set the index to be station names
print(bike_station_df.head())

# ------------------------------------------------------------------------------

bike_station_df.to_csv('clustered_bike_data.csv')
