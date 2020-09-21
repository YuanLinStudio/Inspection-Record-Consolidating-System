import pandas

from JsonService import JsonService

jsonService = JsonService()

dataFrame = pandas.read_csv('车站.csv', usecols=[1, 2])
dataFrame.dropna(inplace=True)

stations = dict()

for index, row in dataFrame.iterrows():

    stations[row['站点']] = str('%d号线' % row['归属线路'])
    stations[str('%s站' % row['站点'])] = str('%d号线' % row['归属线路'])

jsonService.save('stations.json', stations)

print(stations)
