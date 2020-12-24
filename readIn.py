import pandas


def readIn(filename):
    '''
    dataFrame = pandas.read_csv(
        filename, parse_dates=['开始答题时间', '结束答题时间'])
    '''

    dataFrame = pandas.read_excel(
        filename, engine='openpyxl', parse_dates=['开始答题时间', '结束答题时间'])

    # 将 NA 单元格填充为 ''
    dataFrame = dataFrame.fillna('')

    return dataFrame


if __name__ == '__main__':
    # 执行入口

    dataFrame = readIn(
        r'C:\Users\yuanl\OneDrive\桌面\4165188_202012231606191200.xlsx')
    print(dataFrame)
