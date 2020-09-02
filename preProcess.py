import pandas
from datetime import datetime


def preProcess(dataFrame):

    # 列识别

    # 检查日期多列合并
    dataFrame['date'] = dataFrame['2.检查日期:请选择'] + \
        dataFrame['2.检查日期:请选择.1'] + dataFrame['2.检查日期:请选择.2']

    # 检查日期“今天”的替换
    dataFrame['检查日期'] = dataFrame['开始答题时间'].dt.date
    for index, row in dataFrame.iterrows():
        if row['date'] != '今天':
            dataFrame.loc[index, '检查日期'] = datetime.strptime(
                row['date'], '%Y年%m月%d日').date()

    # 删除备用列
    dataFrame.drop(['date'], axis=1, inplace=True)

    return dataFrame
