import os

from common import get_file_name, data_file_exists


def process_data(year):
    pass


def main():
    process_data(2019)


if __name__ == "__main__":
    directory = os.getcwd().split(os.sep)[-1]
    if (os.path.isfile("./process_data.py") and directory == "omie"):
        main()
    else:
        raise Exception("Must run file in same directory as file")
