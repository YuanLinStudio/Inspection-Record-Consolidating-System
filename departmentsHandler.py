import pandas

from JsonService import loadJson, saveJson

dataFrame = pandas.read_csv('责任单位.csv')
dataFrame.dropna(inplace=True)

departments = dict()

for index, row in dataFrame.iterrows():

    departments[row['线路']] = row['责任单位']

saveJson('departments.json', departments)

print(departments)
