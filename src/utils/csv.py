import pandas as pd
from statistics import median


def get_ck_data(path: str):

    data_frame = pd.read_csv(path)

    loc_arr = []
    cbo_arr = []
    dit_arr = []
    wmc_arr = []

    for index, row in data_frame.iterrows():
        loc_arr.append(row['loc'])
        cbo_arr.append(row['cbo'])
        dit_arr.append(row['dit'])
        wmc_arr.append(row['wmc'])

    return {
        'loc': sum(loc_arr, 0),
        'cbo': median(cbo_arr),
        'dit': median(dit_arr),
        'wmc': median(wmc_arr),
    }


def save_repos_to_csv(data: list, path: str, mode='w'):
    data_frame = pd.DataFrame([item.__dict__ for item in data])

    data_frame.to_csv(path, mode=mode, header=False)
