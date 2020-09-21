import pandas

from JsonService import JsonService

jsonService = JsonService()

dataFrame = pandas.read_csv('列识别.csv')
dataFrame.dropna(inplace=True)

columnRecognizer = dict()

for index, row in dataFrame.iterrows():

    columnRecognizer[row['原始列']] = row['标准列']

jsonService.save('columnRecognizer.json', columnRecognizer)

print(columnRecognizer)
