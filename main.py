import numpy
import pandas

from Preprocess import Preprocess
from Process import Process
from readIn import readIn
from AttachmentMatch import AttachmentMatch
from JsonService import JsonService
from Postprocess import Postprocess

jsonService = JsonService()

originalDataFrame = readIn('4165188.csv')

preprocess = Preprocess()

originalDataFrame = preprocess.operate(originalDataFrame)

process = Process()

originalDataFrame = process.operate(originalDataFrame)

postprocess = Postprocess()

dataFrame = postprocess.operate(originalDataFrame)

attachmentMatch = AttachmentMatch()

dataFrame = attachmentMatch.operate(dataFrame, r'C:\Users\yuanl\Downloads\腾讯问卷\问卷#4165188 - 西安地铁服务监督员检查记录提交系统')

attachmentDict = attachmentMatch.getHashDict()
jsonService.save('attachment.json', attachmentDict)

dataFrame = postprocess.reorderAfterAttachmentMatch(dataFrame)

print(originalDataFrame.info())

originalDataFrame.to_csv('1.csv', encoding="utf_8_sig", index=False)
dataFrame.to_csv('2.csv', encoding="utf_8_sig", index=False)
# print(originalDataFrame.columns.values)
