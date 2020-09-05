from datetime import datetime

import pandas


class Preprocess:

    dataFrame = []

    def start(self, dataFrame):

        self.dataFrame = dataFrame

        # 重命名列
        self.columnRename()

        # 是否发现了问题列
        self.isIssueFound()

        # 去除上/下行标记
        self.removeBounds()

        # 附件个数
        self.attachmentCount()

        # 检查日期和时间列合并
        self.columnMerge()

        # 处理“今天”和“现在”
        self.todayToDate()
        self.nowToTime()

        # 监督员备注
        self.commentToDescription()

        return self.dataFrame

    def columnRename(self):

        columnRenameDict = {'编号': '原始记录编号',
                            '1.服务监督员编号或姓名': '服务监督员编号或姓名',
                            '3.检查地点:请选择': '检查地点位置',
                            '3.检查地点:请选择.1': '检查地点线路',
                            '3.检查地点:请选择.2': '检查地点',
                            '6.问题描述': '问题描述',
                            '7.问题类型及分类:请选择': '问题类型',
                            '7.问题类型及分类:请选择.1': '问题分类',
                            '10.附件': '附件 1',
                            '11.附件': '附件 2'}

        self.dataFrame.rename(columns=columnRenameDict, inplace=True)

    def isIssueFound(self):

        self.dataFrame['是否发现问题'] = self.dataFrame['4.您本次检查是否发现了问题？'].apply(
            lambda text: '发现了问题' in text)

        self.dataFrame.drop(['4.您本次检查是否发现了问题？'], axis=1, inplace=True)

    def removeBounds(self):
        self.dataFrame['检查地点'] = self.dataFrame['检查地点'].apply(
            lambda text: text.replace('（上行）', '').replace('（下行）', ''))

    def attachmentCount(self):

        self.dataFrame['附件个数'] = self.dataFrame.apply(
            lambda dataFrame: self.__attachmentCount(dataFrame['附件 1'], dataFrame['附件 2']), axis=1)

        self.dataFrame.drop(['9.请您选择本次检查共计划提交几份附件'], axis=1, inplace=True)

    def __attachmentCount(self, attachment1, attachment2) -> str:

        count = 0

        if attachment1 != '':

            count += 1

        if attachment2 != '':

            count += 1

        return '%d' % count

    def columnMerge(self):

        # 检查日期多列合并
        self.dataFrame['日期'] = self.dataFrame['2.检查日期:请选择'] + \
            self.dataFrame['2.检查日期:请选择.1'] + self.dataFrame['2.检查日期:请选择.2']

        # 发生时间多列合并
        self.dataFrame['时间'] = self.dataFrame['5.发生时间（或发现时间）:请选择'] + \
            self.dataFrame['5.发生时间（或发现时间）:请选择.1']

        self.dataFrame.drop(['2.检查日期:请选择', '2.检查日期:请选择.1', '2.检查日期:请选择.2',
                             '5.发生时间（或发现时间）:请选择', '5.发生时间（或发现时间）:请选择.1'], axis=1, inplace=True)

    def todayToDate(self):

        # 检查日期“今天”的替换
        self.dataFrame['检查日期'] = self.dataFrame.apply(
            lambda dataFrame: self.__todayToDate(dataFrame['开始答题时间'], dataFrame['日期']), axis=1)

        self.dataFrame.drop(['日期'], axis=1, inplace=True)

    def __todayToDate(self, timeStart, date) -> str:

        if date == '今天':

            result = timeStart.date()

        else:

            result = datetime.strptime(date, '%Y年%m月%d日').date()

        return result

    def nowToTime(self):

        # 发生时间“现在”的替换
        self.dataFrame['检查时间'] = self.dataFrame.apply(
            lambda dataFrame: self.__nowToTime(dataFrame['开始答题时间'], dataFrame['时间']), axis=1)

        self.dataFrame.drop(['时间'], axis=1, inplace=True)

    def __nowToTime(self, timeStart, time) -> str:

        if time == '':

            result = ''

        elif time == '现在':

            result = timeStart.strftime('%H时%M分许')

        else:

            result = time

        return result

    def commentToDescription(self):

        self.dataFrame['问题描述'] = self.dataFrame.apply(
            lambda dataFrame: self.__commentToDescription(dataFrame['问题描述'], dataFrame['8.备注']), axis=1)

        self.dataFrame.drop(['8.备注'], axis=1, inplace=True)

    def __commentToDescription(self, description, comment) -> str:

        result = description

        if comment != '':

            result += '[监督员备注]  '
            result += comment

        return result
