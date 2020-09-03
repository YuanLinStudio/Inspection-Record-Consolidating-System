import pandas

from JsonService import loadJson, saveJson

dataFrame = pandas.read_csv('监督员编号对照表.csv')
dataFrame.dropna(inplace=True)

supervisors = dict()

for index, row in dataFrame.iterrows():

    supervisors[row['姓名']] = row['编号']

saveJson('supervisors.json', supervisors)

print(supervisors)
