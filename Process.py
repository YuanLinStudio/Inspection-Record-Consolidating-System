import pandas

from JsonService import loadJson


class Process:

    dataFrame = []

    def __init__(self):
        self.stations = loadJson'stations.json')

    def start(self, dataFrame):
        self.dataFrame = dataFrame

        self.__lineInCharge()

        return self.dataFrame

    def __lineInCharge(self):

        self.dataFrame['线别'] = ''

        for index, row in self.dataFrame.iterrows():

            if row['检查地点位置'] == '车站':

                self.dataFrame.loc[index, '线别'] = self.stations.get(row['检查地点站点'])

            elif row['检查地点位置'] == '列车上':

                self.dataFrame.loc[index, '线别'] = row['检查地点线路']

            elif row['检查地点位置'] == '其他位置':

                self.dataFrame.loc[index, '线别'] = '其他'

    def __supervisorID(self):
        pass
