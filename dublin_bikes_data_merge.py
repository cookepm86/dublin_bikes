
import json

import datetime

# ------------------------------------------------------------------------------

# read in the data and store as a list
file_list = ['data_SatSun.json', 'data_SunMon.json', 'data_Tue.json']
data_list = []

for f in file_list:
    with open(f, 'r') as infile:
        data = json.load(infile)
    data_list.append(data)

# ------------------------------------------------------------------------------

def round_30(x):
    """
    function to round time to nearest 30 mins
    and to identify data by date and weekday

    returns tuple of date, day of the week (numeric)
    and time (rounded to nearest 30 mins)
    """
    x_dt = datetime.datetime.strptime(x, '%Y%m%d %H:%M:%S')
    base = datetime.datetime(x_dt.year, x_dt.month, x_dt.day, x_dt.hour,0)
    delta = datetime.timedelta(minutes=30*round((float(x_dt.minute)
                + float(x_dt.second)/60) / 30))

    return x[:8], x_dt.weekday(), (base + delta).strftime('%H%M')

# ------------------------------------------------------------------------------

# we define a dictionary into which we merge all the data
data_dict = dict.fromkeys(['weekday', 'weekend'])
# fill these with sub-dictionaries
data_dict['weekday'] = dict.fromkeys(['mon', 'tue', 'wed', 'thu', 'fri'])
data_dict['weekend'] = dict.fromkeys(['sat', 'sun'])

# initialize lists for each entry
for key in data_dict.keys():
    for subkey in data_dict[key].keys():
        data_dict[key][subkey] = []

# define a useful conversion dictionary
conversion_dict = {0:'mon', 1:'tue', 2:'wed', 3:'thu', 4:'fri',
                    5:'sat', 6:'sun'}

# ------------------------------------------------------------------------------

for dataset in data_list:

    # clean the timestamps
    time_data_clean = [round_30(x[0]) for x in dataset]
    # store all of the bike data as a list
    bike_data_list = [x[1] for x in dataset]
    # zip the two above lists back together
    data_clean = [x for x in zip(time_data_clean, bike_data_list)]

    # store data in the dictionary
    for datapoint in data_clean:
        # define day
        day_numeric = datapoint[0][1]
        day = conversion_dict[day_numeric]
        if day_numeric > 4:
            data_dict['weekend'][day].append((datapoint[0][0],
                                                datapoint[0][2], datapoint[1]))
        else:
            data_dict['weekday'][day].append((datapoint[0][0],
                                                datapoint[0][2], datapoint[1]))

# store the data
with open('merged_data', 'w') as outfile:
    json.dump(data_dict, outfile)
