import pandas
from datetime import datetime


class Preprocess:

    dataFrame = []  # 列

    def __init__(self, dataFrame):

        self.dataFrame = dataFrame

    def preprocess(self):

        # 列合并
        self.columnMerge()

        # 重命名列
        self.columnRename()

        '''
        # 检查日期“今天”的替换
        dataFrame['检查日期'] = dataFrame['开始答题时间'].dt.date
        for index, row in dataFrame.iterrows():
            if row['date'] != '今天':
                dataFrame.loc[index, '检查日期'] = datetime.strptime(
                    row['date'], '%Y年%m月%d日').date()

        # 删除备用列
        dataFrame.drop(['date'], axis=1, inplace=True)'''

    '''
    def columnRecognize(dataFrame) -> dict:

        columnIndex = dict()

        columnNames = dataFrame.columns.tolist()

        columnNamesToRecognize = ['开始答题时间']

        columnIndex['开始答题时间'] = [i for i, j in enumerate(columnNames) if '开始答题时间' in j]
        columnIndex['检查日期'] = [i for i, j in enumerate(columnNames) if '检查日期' in j]

        return columnIndex
    '''

    def columnRename(self):

        columnRenameDict = {'编号': '原始记录编号',
                            '1.服务监督员编号或姓名': '服务监督员编号或姓名',
                            '3.检查地点:请选择': '检查地点位置',
                            '3.检查地点:请选择.1': '检查地点线路',
                            '3.检查地点:请选择.2': '检查地点站点',
                            '4.您本次检查是否发现了问题？': '是否发现问题',
                            '6.问题描述': '问题描述',
                            '7.问题类型及分类:请选择': '问题类型',
                            '7.问题类型及分类:请选择.1': '问题分类',
                            '8.备注': '监督员备注',
                            '9.请您选择本次检查共计划提交几份附件': '附件个数',
                            '10.附件': '附件 1',
                            '11.附件': '附件 2'}

        self.dataFrame.rename(columns=columnRenameDict, inplace=True)

    def columnMerge(self):

        # 检查日期多列合并
        self.dataFrame['日期'] = self.dataFrame['2.检查日期:请选择'] + \
            self.dataFrame['2.检查日期:请选择.1'] + self.dataFrame['2.检查日期:请选择.2']

        # 发生时间多列合并
        self.dataFrame['时间'] = self.dataFrame['5.发生时间（或发现时间）:请选择'] + \
            self.dataFrame['5.发生时间（或发现时间）:请选择.1']

