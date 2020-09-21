from datetime import datetime

import pandas

from JsonService import JsonService


class Preprocess:

    dataFrame = []

    def __init__(self):

        self.jsonService = JsonService()

        self.columnRecognizer = self.jsonService.load('columnRecognizer.json')

    def operate(self, dataFrame):

        self.dataFrame = dataFrame

        # 重命名列
        self.columnRename()

        # 数据版本
        self.version()

        # 是否发现了问题列
        self.isIssueFound()

        # 去除上/下行标记
        self.removeBounds()

        # 处理其他问题类型和待评定问题分类
        self.undefinedCategory()
        self.undefinedType()

        # 附件个数
        self.attachmentCount()

        # 附件移位，若前者为空则前移
        self.attachmentSort()

        # 检查日期和时间列合并
        self.columnMerge()

        # 处理“今天”和“现在”
        self.todayToDate()
        self.nowToTime()

        # 监督员备注
        self.commentToDescription()

        return self.dataFrame

    def columnRename(self):

        self.dataFrame.rename(columns=self.columnRecognizer, inplace=True)

    def version(self):

        self.dataFrame['数据版本'] = self.dataFrame.apply(
            lambda dataFrame: self.__version(dataFrame['开始答题时间']), axis=1)

    def __version(self, timeStart):

        currentVersion = '20190801'
        timeVersion = datetime.strptime(currentVersion, '%Y%m%d').date()

        if timeStart >= timeVersion:

            return '20190801'

    def isIssueFound(self):

        self.dataFrame['是否发现问题'] = self.dataFrame['4.您本次检查是否发现了问题？'].apply(
            lambda text: '发现了问题' in text)

        self.dataFrame.drop(['4.您本次检查是否发现了问题？'], axis=1, inplace=True)

    def removeBounds(self):

        self.dataFrame['检查地点'] = self.dataFrame['检查地点'].apply(
            lambda text: text.replace('（上行）', '').replace('（下行）', ''))

    def undefinedCategory(self):

        self.dataFrame['问题分类'] = self.dataFrame['问题分类'].apply(
            lambda text: text.replace('未列出', ''))

    def undefinedType(self):

        self.dataFrame['问题类型'] = self.dataFrame['问题类型'].apply(
            lambda text: text.replace('其他未列出的问题类型', '其他'))

    def attachmentCount(self):

        self.dataFrame['附件个数'] = self.dataFrame.apply(
            lambda dataFrame: self.__attachmentCount(dataFrame['附件 1'], dataFrame['附件 2']), axis=1)

    def __attachmentCount(self, attachment1, attachment2) -> str:

        count = 0

        if attachment1 != '':

            count += 1

        if attachment2 != '':

            count += 1

        return count

    def attachmentSort(self):

        self.dataFrame['附件 1'], self.dataFrame['附件 2'] = zip(*self.dataFrame.apply(
            lambda dataFrame: self.__attachmentSort(dataFrame['附件 1'], dataFrame['附件 2']), axis=1))

    def __attachmentSort(self, attachment1, attachment2) -> (str, str):

        if attachment1 == '' and attachment2 != '':

            attachment1, attachment2 = attachment2, attachment1

        return attachment1, attachment2

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
