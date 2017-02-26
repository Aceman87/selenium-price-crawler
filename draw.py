import re
from currency_converter import CurrencyConverter
from datetime import datetime
from plotly.offline import plot
import plotly.graph_objs as go

class Drawer:

    def __init__(self, datafile):
        self.title_text = 'Price development'
        self.filename = 'price_graph.html'
        self.currency = 'EUR'
        self.datafile = datafile
        self.non_letter = re.compile(r'[^\d.,]+')
        self.data = self.parse_data()

    def draw_scatter(self):
        plot_data = []
        for key in self.data.keys():
            new_trace = go.Scatter(
                x = self.data[key]['x'],
                y = self.data[key]['y'],
                mode = key,
                name = key
            )
            plot_data.append(new_trace)
        plot(plot_data, filename=self.filename, auto_open=False)

    def parse_data(self):
        c = CurrencyConverter('http://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip')
        traces = {}
        with open(self.datafile, 'r') as f: 
            for line in f: 
                data_split = line.split('|', 3 )

                # Create a new dictionary for the id in data_split[0] if there is none
                if traces.get(data_split[0]) == None:
                    traces[data_split[0]] = {'x':[],'y':[]}

                # Parse a time from the time string
                data_split[1] = datetime.strptime(data_split[1],"%d.%m.%Y_%H:%M")
                # Remove letters from the price
                data_split[2] = self.non_letter.sub('', data_split[2])
                # Parse the price into a float
                data_split[2] = self.parse_price(data_split[2])
                data_split[3] = data_split[3].rstrip('\n')
                # Convert currency if needed
                if data_split[3] != self.currency:
                    #print ("Converting currency: ", data_split[2], data_split[3], self.currency)
                    data_split[2] = c.convert(data_split[2], data_split[3], self.currency)

                # Add the data to the x and y lists in the dictionary
                # {id1: {x: [date1,date2...], y:[price1,price2...]}, id2: {x: [date1,date2...], y:[price1,price2...]}}
                traces[data_split[0]]['x'].append(data_split[1])
                traces[data_split[0]]['y'].append(data_split[2])
        return traces

    # https://stackoverflow.com/questions/41023295/looking-for-an-universal-way-to-parse-price-into-decimal
    def parse_price(self, s):
        if '.' not in s and ',' not in s:
            return float(s)

        elif s[-3] in ',.':
            dec_char = s[-3]
            sep_char = {'.': ',', ',':'.'}[dec_char]
            s = s.replace(sep_char, '')
            s = s.replace(',', '.')
            return float(s)

        else:
            s = s.replace(',','').replace('.', '')
            return float(s)