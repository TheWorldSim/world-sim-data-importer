import os


def get_file_name(**kwargs):
    return "./data/{year}_{month}_{day}.txt".format(**kwargs)


def data_file_exists(**kwargs):
    file_name = get_file_name(**kwargs)
    return os.path.isfile(file_name)
