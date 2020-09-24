import os
import sys
import time

import numpy
import pandas
from PyQt5 import QtCore, QtGui, QtWidgets

from AttachmentMatch import AttachmentMatch
from JsonService import JsonService
from MainWindow import MainWindow
from MessageWindow import MessageWindow
from Postprocess import Postprocess
from Preprocess import Preprocess
from Process import Process
from readIn import readIn


class WindowController:

    def __init__(self):
        '''
        初始化
        新建对象时默认执行
        '''

        # ## 窗口

        # 主窗口
        self.mainWindow = MainWindow()

        # 信息窗口
        self.informationMessageApp = QtWidgets.QWidget()
        self.informationMessageWindow = MessageWindow()

        # 服务项
        self.preprocess = Preprocess()
        self.process = Process()
        self.postprocess = Postprocess()
        self.attachmentMatch = AttachmentMatch()
        self.jsonService = JsonService()

        self.settingJsonService = JsonService('settings.json')

        # ## 连接 Slots 和 Signals

        # 快速处理: 更改 --> 快速处理
        self.mainWindow.expressProcessButton.pressed.connect(
            self.expressProcess)

    def show(self):
        '''
        启动主窗口
        '''

        # 设置部分项不可见

        self.mainWindow.qrCodeButton.setVisible(False)
        self.mainWindow.commandButton.setVisible(False)

        # 从 settings.json 取值更新窗口
        self.updateLastProcess()

        self.mainWindow.show()

    def updateLastProcess(self):
        '''
        从 settings.json 取值更新窗口
        '''

        lastProcessDict = self.settingJsonService.get('last process')

        if lastProcessDict is not None:

            # 若无上次记录，则隐藏 last process widget
            self.mainWindow.lastProcessWidget.setVisible(
                lastProcessDict['time'] != '')

            self.mainWindow.lastProcessTimeLabel.setText(
                lastProcessDict['time'])
            self.mainWindow.lastProcessTotalRecordsLabel.setText(
                str(lastProcessDict['total records']))
            self.mainWindow.lastProcessValidRecordsLabel.setText(
                str(lastProcessDict['valid records']))
            self.mainWindow.lastProcessAttachmentsCountLabel.setText(
                str(lastProcessDict['attachments count']))

    def informationMessage(self, message='系统运行中', autoClose=3):
        '''
        显示信息

        参数值：
            message (str): 提示
            autoClose (int): 自动关闭时长 / s
        '''

        self.informationMessageWindow.setMessage(message)
        self.informationMessageWindow.setAutoClose(autoClose)
        self.informationMessageWindow.show()

    def exceptionMessage(self, exception=None, message='系统遇到了一些错误', autoClose=3):
        '''
        显示错误信息

        参数值：
            exception (exception): 异常对象
            message (str): 提示
            autoClose (int): 自动关闭时长 / s
        '''

        if exception is not None:
            print(exception.args)
            message += '\n\n'
            message += str(exception.args)

        # 新建信息窗口
        self.informationMessage(message, autoClose)

    def expressProcess(self):
        '''
        快速处理
        '''

        # ## 文件读入和处理

        # 选取原始记录文件

        originalDataFile, filetype = QtWidgets.QFileDialog.getOpenFileName(
            self.mainWindow, '选择原始记录文件', '/', 'All Files (*.*);;CSV (Comma delimited) (*.csv)')
        print(originalDataFile)

        # 选择校验和文件格式校验

        if originalDataFile is None or originalDataFile == '':

            return

        filetype = originalDataFile.split('.')[-1]

        if filetype != 'csv' and filetype != 'CSV':

            self.informationMessage('文件格式错误，请选择 *.csv 格式的文件')

            return

        # 开始处理

        originalDataFrame = readIn(originalDataFile)

        originalDataFrame = self.preprocess.operate(originalDataFrame)
        originalDataFrame = self.process.operate(originalDataFrame)
        dataFrame = self.postprocess.operate(originalDataFrame)

        # ## 附件匹配

        shouldAttachmentMatch = True  # 是否要进行附件匹配的标志

        # 选取附件所在的文件夹

        attachmentDir = QtWidgets.QFileDialog.getExistingDirectory(
            self.mainWindow, '选取附件所在的文件夹', '/')

        # 选择校验和文件格式校验

        if attachmentDir is None or attachmentDir == '':

            self.informationMessage('未选择附件所在文件夹，本次结果将不进行附件匹配', 10)

            shouldAttachmentMatch = False

        # 附件匹配

        if shouldAttachmentMatch is True:

            dataFrame = self.attachmentMatch.operate(dataFrame, attachmentDir)

            attachmentDict = self.attachmentMatch.getHashDict()
            self.jsonService.save('attachment.json', attachmentDict)

            dataFrame = self.postprocess.reorderAfterAttachmentMatch(dataFrame)

        print(dataFrame.info())

        # ## 保存处理结果

        # 选取保存目录

        exportFile, filetype = QtWidgets.QFileDialog.getSaveFileName(
            self.mainWindow, '选择保存处理结果的目录', '/服务数据汇总表.csv', 'CSV (Comma delimited) (*.csv)')

        # 选择校验和文件格式校验

        if exportFile is None or exportFile == '':

            self.informationMessage('未选择保存目录，本次结果未保存')

            return

        dataFrame.to_csv(exportFile, encoding="utf_8_sig", index=False)

        # ## 更新 settings.json 文件

        thisProcessDetail = dict()

        # 处理时间
        timeStamp = time.strftime('%Y-%m-%d %H:%M:%S',
                                  time.localtime(time.time()))
        thisProcessDetail['time'] = timeStamp

        # 全部记录
        totalRecords = originalDataFrame.shape[0]
        thisProcessDetail['total records'] = totalRecords

        # 有效记录
        validRecords = dataFrame.shape[0]
        thisProcessDetail['valid records'] = validRecords

        # 有效附件
        if self.attachmentMatch.archivedPath != '':
            attachmentsCount = len(os.listdir(
                self.attachmentMatch.archivedPath))
        else:
            attachmentsCount = 0
        thisProcessDetail['attachments count'] = attachmentsCount

        self.settingJsonService.set('last process', thisProcessDetail)

        self.informationMessage('快速处理成功')

        # 从 settings.json 取值更新窗口
        self.updateLastProcess()


if __name__ == '__main__':
    # 执行入口

    # 设置高分辨率屏幕行为
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.AA_EnableHighDpiScaling)  # 支持高分辨率屏幕
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.AA_UseHighDpiPixmaps)  # 使用高分辨率图标

    # 程序载入
    app = QtWidgets.QApplication(sys.argv)
    windowController = WindowController()
    windowController.show()
    sys.exit(app.exec_())
