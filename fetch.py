import hashlib
import time
import os
from draw import Drawer
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Fetcher:

    def __init__(self, options):
        # file handle
        self.file_txt_path = os.path.join(options['output_directory'], options['file_name'])
        self.input_data = options['data'] 

    def run(self):
        print("Creating driver...")
        driver = self.create_selenium_driver()

        output = []
        for data in self.input_data:
            print("Getting URL",len(output)+1,"...")
            driver.get(data[0])
            price_time = time.strftime("%d.%m.%Y_%H:%M", time.localtime())
            price_element = driver.find_element_by_id(data[1])

            price_data = []
            unicode_url = data[0].encode('utf-8')
            price_data.append(hashlib.md5(unicode_url).hexdigest())
            price_data.append(price_time)
            price_data.append(price_element.text)
            price_data.append(data[2])
            output.append(price_data)
            #print (price_element.text)

        print("Writing to file...")
        with open(self.file_txt_path, 'a') as f:
            for price_data in output:
                f.write(price_data[0] + '|' + price_data[1] + '|' + price_data[2] + '|' + price_data[3])
                f.write('\n')

        print("Plotting graph...")
        drawer = Drawer(self.file_txt_path)
        drawer.draw_scatter()
        print ('Done')

    def create_selenium_driver(self):
        #return webdriver.Firefox()
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
        )
        driver = webdriver.PhantomJS(desired_capabilities=dcap)
        driver.set_window_size(1024, 768)
        return driver