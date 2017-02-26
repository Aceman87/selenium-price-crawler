class Loader:

    def __init__(self):
        self.output = []

    def load_data(self, datafile):
        with open(datafile, 'r') as f: 
            for line in f:
                #strip line changes and split into three parts by '|'
                data_split = line.rstrip('\n').split('|', 3 )
                self.output.append(data_split)
        return self.output