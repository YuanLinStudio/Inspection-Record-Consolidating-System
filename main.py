import numpy
import pandas

from Preprocess import Preprocess
from Process import Process
from readIn import readIn

originalDataFrame = readIn('4165188.csv')

preprocess = Preprocess()

originalDataFrame = preprocess.start(originalDataFrame)

process = Process()

originalDataFrame = process.start(originalDataFrame)


print(originalDataFrame.info())
'''
print(originalDataFrame['开始答题时间'][4]>originalDataFrame['开始答题时间'][5])
print(originalDataFrame['开始答题时间'])
print(originalDataFrame)
print(originalDataFrame['检查日期'])
'''
originalDataFrame.to_csv('1.csv', encoding="utf_8_sig")
# print(originalDataFrame.columns.values)
