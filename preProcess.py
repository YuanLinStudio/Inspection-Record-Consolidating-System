from datetime import datetime

import pandas


class Preprocess:

    dataFrame = []

    def start(self, dataFrame):

        self.dataFrame = dataFrame

        # 重命名列
        self.__columnRename()

        # 是否发现了问题列
        self.__isIssueFound()

        # 附件个数
        self.__attachmentCount()

        # 检查日期和时间列合并
        self.__columnMerge()

        # 处理“今天”和“现在”
        self.__todayToDate()
        self.__nowToTime()

        # 监督员备注
        self.__commentToDescription()

        return self.dataFrame

    def __columnRename(self):

        columnRenameDict = {'编号': '原始记录编号',
                            '1.服务监督员编号或姓名': '服务监督员编号或姓名',
                            '3.检查地点:请选择': '检查地点位置',
                            '3.检查地点:请选择.1': '检查地点线路',
                            '3.检查地点:请选择.2': '检查地点站点',
                            '6.问题描述': '问题描述',
                            '7.问题类型及分类:请选择': '问题类型',
                            '7.问题类型及分类:请选择.1': '问题分类',
                            '10.附件': '附件 1',
                            '11.附件': '附件 2'}

        self.dataFrame.rename(columns=columnRenameDict, inplace=True)

    def __isIssueFound(self):

        self.dataFrame['是否发现问题'] = self.dataFrame['4.您本次检查是否发现了问题？'].apply(
            lambda text: '发现了问题' in text)

        self.dataFrame.drop(['4.您本次检查是否发现了问题？'], axis=1, inplace=True)

    def __attachmentCount(self):

        self.dataFrame['附件个数'] = 0

        for index, row in self.dataFrame.iterrows():

            if row['附件 1'] != '':

                self.dataFrame.loc[index, '附件个数'] += 1

            if row['附件 2'] != '':

                self.dataFrame.loc[index, '附件个数'] += 1

            # 若第 1 附件位为空而第 2 附件位非空，则将附件内容前移
            if row['附件 1'] == '' and row['附件 2'] != '':

                self.dataFrame.loc[index,
                                   '附件 1'] = self.dataFrame.loc[index, '附件 2']
                self.dataFrame.loc[index, '附件 2'] = ''

        self.dataFrame.drop(['9.请您选择本次检查共计划提交几份附件'], axis=1, inplace=True)

    def __columnMerge(self):

        # 检查日期多列合并
        self.dataFrame['日期'] = self.dataFrame['2.检查日期:请选择'] + \
            self.dataFrame['2.检查日期:请选择.1'] + self.dataFrame['2.检查日期:请选择.2']

        # 发生时间多列合并
        self.dataFrame['时间'] = self.dataFrame['5.发生时间（或发现时间）:请选择'] + \
            self.dataFrame['5.发生时间（或发现时间）:请选择.1']

        self.dataFrame.drop(['2.检查日期:请选择', '2.检查日期:请选择.1', '2.检查日期:请选择.2',
                             '5.发生时间（或发现时间）:请选择', '5.发生时间（或发现时间）:请选择.1'], axis=1, inplace=True)

    def __todayToDate(self):

        # 检查日期“今天”的替换
        self.dataFrame['检查日期'] = self.dataFrame['开始答题时间'].dt.date

        for index, row in self.dataFrame.iterrows():

            if row['日期'] != '今天':

                self.dataFrame.loc[index, '检查日期'] = datetime.strptime(
                    row['日期'], '%Y年%m月%d日').date()

        self.dataFrame.drop(['日期'], axis=1, inplace=True)

    def __nowToTime(self):

        # 发生时间“现在”的替换
        self.dataFrame['检查时间'] = self.dataFrame['开始答题时间'].apply(
            lambda datetime: datetime.strftime('%H时%M分许'))

        for index, row in self.dataFrame.iterrows():

            if row['时间'] == '':

                self.dataFrame.loc[index, '检查时间'] = ''

            elif row['时间'] != '现在':

                self.dataFrame.loc[index, '检查时间'] = row['时间']

        self.dataFrame.drop(['时间'], axis=1, inplace=True)

    def __commentToDescription(self):

        for index, row in self.dataFrame.iterrows():

            if row['8.备注'] != '':

                self.dataFrame.loc[index,
                                   '问题描述'] += '[监督员备注]  '
                self.dataFrame.loc[index,
                                   '问题描述'] += self.dataFrame.loc[index, '8.备注']

        self.dataFrame.drop(['8.备注'], axis=1, inplace=True)
