import pandas


def readIn(filename):

    dataFrame = pandas.read_csv(
        filename, parse_dates=['开始答题时间', '结束答题时间'])

    dataFrame = dataFrame.fillna('')

    return dataFrame
