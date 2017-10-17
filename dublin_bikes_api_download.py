import sched, time
import requests
import json

import datetime

# ------------------------------------------------------------------------------

filename = 'data_SatSun.json'

# ------------------------------------------------------------------------------

class download_data(object):
    """
    class to download data at periodic time intervals
    """

    data_list = []

    def __init__(self, url, api_key, delta_t=1800, total_t=1800):
        """
        returns a download object whose attributes are the url of
        the website, the api key to download the data, the periodicity
        of the download cycle and the total time to perform this task for
        """
        self.url = url
        self.api_key = api_key
        self.delta_t = delta_t
        self.total_t = total_t
        # initialize a list for downloaded data to be stored in

    def run(self):
        """
        runs download task for specified time period and periodicity
        from website with given api key
        """

        def download():
            """
            function which downloads data from url, url, with api key, api_key
            """
            # set the request parameters
            my_url = self.url + '&apiKey=' + self.api_key
            user = 'admin'
            pwd = 'admin'

            # set proper headers
            headers = {"Accept":"application/json"}

            # perform the HTTP request
            response = requests.get(my_url, auth=(user, pwd), headers=headers)

            # append downloaded json data to data_list
            self.data_list.append((datetime.datetime.now().strftime('%Y%m%d %H:%M:%S'), response.json()))

        def timestamp():
            """
            comment function
            """
            print(datetime.datetime.now().strftime('%Y%m%d %H:%M:%S'), 'step complete')

        def save_as_csv(filepath):
            """
            saves data as csv file
            """

        # initialize scheduler
        sch = sched.scheduler()
        # truncate number of time intervals to integer
        time_period = self.delta_t
        no_time_intervals = int(self.total_t / self.delta_t)
        # execute download at given time periods in total time
        time_list = [t * time_period for t in range(no_time_intervals + 1)]
        for time_stamp in time_list:
            sch.enter(time_stamp, 1, timestamp)
            sch.enter(time_stamp, 2, download)

        # run scheduled tasks
        sch.run()

# ------------------------------------------------------------------------------

dd = download_data('https://api.jcdecaux.com/vls/v1/stations?contract=Dublin',
                     'd2aa5a02f507f8ed4aad52a78772c1496c7cb505', 60*30, 60*60*2)
dd.run()

# ------------------------------------------------------------------------------

with open(filename, 'w') as outfile:
    json.dump(dd.data_list, outfile)
