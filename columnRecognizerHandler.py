import pandas

from JsonService import loadJson, saveJson

dataFrame = pandas.read_csv('列识别.csv')
dataFrame.dropna(inplace=True)

columnRecognizer = dict()

for index, row in dataFrame.iterrows():

    columnRecognizer[row['原始列']] = row['标准列']

saveJson('columnRecognizer.json', columnRecognizer)

print(columnRecognizer)
