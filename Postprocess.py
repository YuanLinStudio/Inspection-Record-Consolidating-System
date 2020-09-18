import pandas


class Postprocess:

    dataFrame = []

    def __init__(self):

        pass

    def operate(self, dataFrame):

        self.dataFrame = dataFrame

        self.filter()
        self.sort()
        self.reorder()

        return self.dataFrame

    def filter(self):
        
        self.dataFrame = self.dataFrame[self.dataFrame['问题描述'] != '']

    def sort(self):

        self.dataFrame = self.dataFrame.sort_values(
            by=['线别', '检查日期', '检查时间'], ascending=[True, True, True])

    def reorder(self):

        self.dataFrame['整改措施'] = ''
        self.dataFrame['是否整改'] = ''
        self.dataFrame['序号'] = range(1, len(self.dataFrame) + 1)

        mainColumns = ['序号', '检查单位', '线别', '检查日期', '检查时间', '检查地点',
                       '问题描述', '问题类型', '问题分类', '责任单位', '整改措施', '附件 1' ,'附件 2', '是否整改']

        detailedColumns = ['原始记录编号', '监督员姓名', '数据版本', '是否发现问题', '附件个数', '开始答题时间', '结束答题时间', '答题时长', '地理位置国家和地区', '地理位置省', '地理位置市', '用户类型', '用户标识', '昵称', '自定义字段']

        self.dataFrame = self.dataFrame[mainColumns + detailedColumns]

    def reorderAfterAttachmentMatch(self, dataFrame) -> pandas.core.frame.DataFrame:

        mainColumns = ['序号', '检查单位', '线别', '检查日期', '检查时间', '检查地点',
                       '问题描述', '问题类型', '问题分类', '责任单位', '整改措施', '附件', '是否整改']

        detailedColumns = ['原始记录编号', '监督员姓名', '数据版本', '是否发现问题', '附件个数', '开始答题时间', '结束答题时间', '答题时长', '地理位置国家和地区', '地理位置省', '地理位置市', '用户类型', '用户标识', '昵称', '自定义字段']

        dataFrame = dataFrame[mainColumns + detailedColumns]

        return dataFrame
