import requests

import os
import time

from common import loop_over_days, get_file_name, data_file_exists


wait_seconds = 10

def fetch_day_of_data(requests_remaining=2, **kwargs):
    url = "https://www.omie.es/sites/default/files/dados/AGNO_{year}/MES_{month}/TXT/INT_D_PFM_DEM_1_{day}_{month}_{year}_{day}_{month}_{year}.TXT".format(**kwargs)
    print("Fetching url: {}".format(url))
    response = requests.get(url)
    requests_remaining -= 1

    if not response.ok and requests_remaining > 0:
        print("Error " + response.status + " fetching url: " + url + "\nResponse text: " + response.text)
        print("Waiting {} seconds before retrying.  {} retries left".format(wait_seconds, requests_remaining))
        time.sleep(wait_seconds)
        fetch_day_of_data(requests_remaining=requests_remaining, **kwargs)

    return response


def store_day_of_data(response, **kwargs):
    file_name = get_file_name(**kwargs)
    with open(file_name, "w") as f:
        f.write(response.text)


def fetch_and_store_day_of_data(date, force_update=False):
    month = str(date.month).zfill(2)
    day = str(date.day).zfill(2)
    date_kwargs = {
        "year": date.year,
        "month": month,
        "day": day,
    }

    if not force_update and data_file_exists(**date_kwargs):
        print("skipping: {year}_{month}_{day}".format(**date_kwargs))
        return

    response = fetch_day_of_data(**date_kwargs)
    response.raise_for_status()

    store_day_of_data(response, **date_kwargs)
    print("Success.  Waiting {} seconds before next request.".format(wait_seconds))
    time.sleep(wait_seconds)


def get_data(year):
    loop_over_days(year, fetch_and_store_day_of_data)


def main():
    get_data(2019)


if __name__ == "__main__":
    directory = os.getcwd().split(os.sep)[-1]
    if (os.path.isfile("./get_data.py") and directory == "omie"):
        main()
    else:
        raise Exception("Must run file in same directory as file")
