'''
处理 CSV 文件为 JSON 文件
'''

import pandas

from JsonService import JsonService


class CsvHandler:
    '''
    处理 CSV 文件为 JSON 文件
    '''

    def __init__(self, csvFile):
        '''
        初始化
        新建对象时默认执行

        参数值：
            csvFile (str): 要读取的 CSV 文件
        '''

        self.jsonService = JsonService()

        self.dataFrame = pandas.read_csv(csvFile)
        self.dataFrame.dropna(inplace=True)

    def operate(self, func, jsonFile):
        '''
        处理 CSV 文件为 JSON 文件

        参数值：
            func (func(dict, row)): 处理规则函数
                函数参数要求：
                    dict(dict): JSON 文件格式
                    row(pandas.series): CSV 文件的每一列
            jsonFile (str): 要存储为的 JSON 文件
        '''

        # 存储属性的 dict
        properties = dict()

        # 循环执行 func
        for index, row in self.dataFrame.iterrows():

            func(properties, row)

        print(properties)

        # 存储到 jsonFile
        self.jsonService.save(jsonFile, properties)


def columnRecognizer(columnRecognizer, row):
    '''
    列识别
    '''

    columnRecognizer[row['原始列']] = row['标准列']


def supervisors(supervisors, row):
    '''
    监督员编号
    '''

    supervisors[row['姓名']] = row['编号']


def stations(stations, row):
    '''
    车站
    '''

    stations[row['站点']] = str('%d号线' % row['归属线路'])
    stations[str('%s站' % row['站点'])] = str('%d号线' % row['归属线路'])


def departments(departments, row):
    '''
    责任单位
    '''

    departments[row['线路']] = row['责任单位']


if __name__ == '__main__':
    # 执行入口

    # 列识别
    columnRecognizerHandler = CsvHandler('列识别.csv')
    columnRecognizerHandler.operate(columnRecognizer, 'cr.json')

    # 监督员编号
    supervisorsHandler = CsvHandler('监督员编号对照表.csv')
    supervisorsHandler.operate(supervisors, 'supervisors.json')

    # 车站
    stationsHandler = CsvHandler('车站.csv')
    stationsHandler.operate(stations, 'stations.json')

    # 责任单位
    departmentsHandler = CsvHandler('责任单位.csv')
    departmentsHandler.operate(departments, 'departments.json')
