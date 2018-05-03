import pandas as pd

data = pd.read_csv('data/s16_pa3_tod_info.csv', header=None)
data.columns = ['TOD', 'hour', 'altitude', 'azimuth', 'PWV', 'cut_status', 'field']

print data
