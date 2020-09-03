import pandas
import numpy

from readIn import readIn
from Preprocess import Preprocess

originalDataFrame = readIn('4165188.csv')

preprocess = Preprocess(originalDataFrame)

preprocess.preprocess()

originalDataFrame = preprocess.dataFrame


print(originalDataFrame.info())
'''
print(originalDataFrame['开始答题时间'][4]>originalDataFrame['开始答题时间'][5])
print(originalDataFrame['开始答题时间'])
print(originalDataFrame)
print(originalDataFrame['检查日期'])
'''
# originalDataFrame.to_csv('1.csv', encoding="utf_8_sig")
# print(originalDataFrame.columns.values)