import csv
import pandas as pd
from src.models.Repo import Repo


def get_ck_data(classPath: str, methodPath: str):
    requiredDict = {}

    with open(classPath, newline='') as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            requiredDict[row['class']] = {
                'cbo': int(row['cbo']), 'dit': int(row['dit']), 'wmc': int(row['wmc']), 'loc': int(row['loc'])}

    with open(methodPath, newline='') as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            requiredDict[row['method']] = {
                'cbo': int(row['cbo']), 'wmc': int(row['wmc']), 'rfc': int(row['rfc']), 'loc': int(row['loc'])}

    return requiredDict


def save_repos_to_csv(data: list, path: str):
    data_frame = pd.DataFrame([item.__dict__ for item in data])

    with open(path, 'w') as file:
        data_frame.to_csv(file)
