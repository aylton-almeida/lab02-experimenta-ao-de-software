import csv


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
