import pandas

from JsonService import JsonService

jsonService = JsonService()

dataFrame = pandas.read_csv('监督员编号对照表.csv')
dataFrame.dropna(inplace=True)

supervisors = dict()

for index, row in dataFrame.iterrows():

    supervisors[row['姓名']] = row['编号']

jsonService.save('supervisors.json', supervisors)

print(supervisors)
