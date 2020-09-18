import pandas

from JsonService import loadJson


class Process:

    dataFrame = []

    def __init__(self):

        self.stations = loadJson('stations.json')
        self.supervisors = loadJson('supervisors.json')
        self.departments = loadJson('departments.json')

        # self.supervisors 的反字典
        self.supervisorsName = {id: name for name,
                                id in self.supervisors.items()}

    def operate(self, dataFrame):

        self.dataFrame = dataFrame

        self.lineInCharge()
        self.supervisorID()
        self.supervisorName()
        self.departmentInCharge()

        return self.dataFrame

    def lineInCharge(self):

        self.dataFrame['线别'] = self.dataFrame.apply(lambda dataFrame: self.__lineInCharge(
            dataFrame['检查地点位置'], dataFrame['检查地点线路'], dataFrame['检查地点']), axis=1)

        self.dataFrame.drop(['检查地点位置', '检查地点线路'], axis=1, inplace=True)

    def __lineInCharge(self, position, line, station) -> str:

        if position == '车站':

            result = self.stations.get(station)

        elif position == '列车上':

            result = line

        elif position == '其他位置':

            result = '其他'

        return result

    def supervisorID(self):

        self.dataFrame['检查单位'] = self.dataFrame.apply(
            lambda dataFrame: self.__supervisorID(dataFrame['服务监督员编号或姓名']), axis=1)

    def __supervisorID(self, string) -> str:

        string = string.strip()

        if string.isdigit():

            id = str('JDY%s' % string)

            if id in self.supervisors.values():

                result = id

            else:

                result = string

        else:

            id = self.supervisors.get(string)

            if id is not None:

                result = id

            else:

                result = string

        return result

    def supervisorName(self):

        self.dataFrame['监督员姓名'] = self.dataFrame.apply(
            lambda dataFrame: self.__supervisorName(dataFrame['检查单位']), axis=1)

    def __supervisorName(self, id) -> str:

        name = self.supervisorsName.get(id)

        if name is not None:

            result = name

        else:

            result = id

        return result

    def departmentInCharge(self):

        self.dataFrame['责任单位'] = self.dataFrame.apply(lambda dataFrame: self.__departmentInCharge(
            dataFrame['线别']), axis=1)

    def __departmentInCharge(self, line) -> str:

        department = self.departments.get(line)

        if department is not None:

            result = department

        else:

            result = ''

        return result
