import pandas

from JsonService import JsonService

jsonService = JsonService()

dataFrame = pandas.read_csv('责任单位.csv')
dataFrame.dropna(inplace=True)

departments = dict()

for index, row in dataFrame.iterrows():

    departments[row['线路']] = row['责任单位']

jsonService.save('departments.json', departments)

print(departments)
