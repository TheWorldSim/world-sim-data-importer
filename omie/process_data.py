import calendar
import csv
from datetime import datetime, timedelta
import os
import re
import sys

from common import loop_over_days, date_to_dict, get_file_name, data_file_exists

data = []


def read_file(file_name):
    with open(file_name, "r") as f:
        return f.read()


def parse_lines_as_floats(text_line):
    values = text_line.replace(",", ".").split(";")[1:-1]
    float_values = [float(v.strip()) for v in values]
    return float_values


def parse_file_contents(file_contents):
    prices = re.search("Precio horario final medio \(EUR/MWh\);[^\n]*", file_contents)[0]
    energies = re.search("Energía \(MWh\);[^\n]*", file_contents)[0]
    price_floats = parse_lines_as_floats(prices)
    energy_floats = parse_lines_as_floats(energies)

    date_data = []

    for (i, price) in enumerate(price_floats):
        hour = i + 1
        energy = energy_floats[i]
        date_data.append([hour, price, energy])

    return date_data


def collect_data(date):
    global data
    date_kwargs = date_to_dict(date)
    file_name = get_file_name(**date_kwargs)

    file_exists = data_file_exists(**date_kwargs)

    if not file_exists:
        print("Warning.  No data file at: " + file_name)
        return

    file_contents = read_file(file_name)
    date_data = parse_file_contents(file_contents)

    date_string = "{year}-{month}-{day}".format(**date_kwargs)

    for hour_data in date_data:
        hour = hour_data[0]
        dt = date + timedelta(hours=hour)
        timestamp = calendar.timegm(dt.timetuple())
        data.append([timestamp, date_string] + hour_data)


def write_to_csv(output_file_name, data):
    with open(output_file_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    print("Wrote {} lines to {}".format(len(data), output_file_name))


def process_data(year):
    global data
    data = [["timestamp", "date", "hour", "average_final_hourly_price_Euros", "energy_(MWh)"]]
    loop_over_days(year, collect_data)
    write_to_csv("./data/aggregated.csv", data)


def main():
    process_data(2019)


if __name__ == "__main__":
    directory = os.getcwd().split(os.sep)[-1]
    if (os.path.isfile("./process_data.py") and directory == "omie"):
        main()
    else:
        raise Exception("Must run file in same directory as file")
