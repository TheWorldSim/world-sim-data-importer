import os
from datetime import datetime, timedelta


def loop_over_days(year, func):
    date = datetime(year, 1, 1)
    next_year = datetime(year + 1, 1, 1)
    one_day = timedelta(days=1)

    while date < next_year:
        func(date)
        date += one_day


def get_file_name(**kwargs):
    return "./data/{year}_{month}_{day}.txt".format(**kwargs)


def data_file_exists(**kwargs):
    file_name = get_file_name(**kwargs)
    return os.path.isfile(file_name)
