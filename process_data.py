"""
Usage:
process_data.py London
process_data.py Beijing
"""

from datetime import timedelta as td, datetime
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Process data to get .csv file containing data for city.')
parser.add_argument('city', type=str,
                    help='city from {"London", "Beijing"}')

args = parser.parse_args()
city = args.city

print(f'Processing data for {city}')

def get_delta(d1, d2):
    delta = d2 - d1
    return delta


file = '[modified] kdd_cup_2018_dataset_missing_values_replaced_with_0.txt'

with open(file, 'r') as f:
    lines = f.readlines()

data = []
for line in lines:
    station_data = line.split(':')
    station_id = station_data[0]
    station_city = station_data[1]
    station_name = station_data[2]
    pollutant = station_data[3]
    date = station_data[4]
    concentrations = station_data[5].split(',')

    hour_range = []
    if station_city == city:
        start_date = '2017-01-01'
        end_date = '2018-03-31'
        d1 = datetime.strptime(start_date, '%Y-%m-%d')
        d2 = datetime.strptime(end_date, '%Y-%m-%d')

        delta = get_delta(d1, d2)
        for i in range(14, delta.days * 24 + 16):
            hour_range.append(d1 + td(hours=i))

    for ts, c in zip(hour_range, concentrations):
        data.append([station_id, station_name, pollutant, ts, c])

df = pd.DataFrame(columns=['station_id', 'station_name', 'pollutant_name', 'timestamp', 'concentration'], data=data)

df.to_csv(f'{city.lower()}_concentrations.csv', index=False)
