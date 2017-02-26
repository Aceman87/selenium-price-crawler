#!/usr/bin/env python3
from draw import Drawer
import os

if __name__ == '__main__':

    options = {
        # Data directory
        'output_directory': "./",
        # Price data file
        'file_name': "watch_prices.txt",
    }
    file_txt_path = os.path.join(options['output_directory'], options['file_name'])
    drawer = Drawer(file_txt_path)
    drawer.draw_scatter()