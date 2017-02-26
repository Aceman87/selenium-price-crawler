#!/usr/bin/env python3
from fetch import Fetcher
from load import Loader

if __name__ == '__main__':

    options = {
        # Prices to fetch list
        'data_file': "fetch_list.txt",
        # Price data file
        'file_name': "watch_prices.txt",
        # Data directory
        'output_directory': "./",
    }
    l = Loader()
    data = l.load_data(options['data_file'])
    options['data'] = data
    w = Fetcher(options)
    w.run()