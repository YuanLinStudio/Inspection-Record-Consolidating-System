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

        # 快速处理/开始: 按下 --> 快速处理
        self.mainWindow.expressProcessButton.pressed.connect(
            self.expressProcess)

        # 开始处理/开始: 按下 --> 一般处理
        self.mainWindow.generalProcessButton.pressed.connect(
            self.generalProcess)

        # 开始处理/原始数据浏览: 按下 --> 选择原始数据文件
        self.mainWindow.generalProcessOriginalDataExploreButton.pressed.connect(
            self.exploreOriginalDataFile)

        # 开始处理/附件目录浏览: 按下 --> 选择附件所在目录
        self.mainWindow.generalProcessAttachmentLocationExploreButton.pressed.connect(
            self.exploreAttachmentDirectory)

        # 开始处理/导出数据浏览: 按下 --> 选择导出数据文件
        self.mainWindow.generalProcessExportFileExploreButton.pressed.connect(
            self.exploreExportDataFile)

    def show(self):
        '''
        启动主窗口
        '''

        # 设置部分项不可见

        self.mainWindow.qrCodeButton.setVisible(False)
        self.mainWindow.commandButton.setVisible(False)

        # 从 settings.json 取值更新窗口
        self.updateWindowWithJson()

        self.mainWindow.show()

    def updateWindowWithJson(self):
        '''
        从 settings.json 取值更新窗口
        '''

        # 路径和目录
        self.mainWindow.generalProcessOriginalDataDirLineEdit.setText(
            self.settingJsonService.get('original data file'))
        self.mainWindow.generalProcessAttachmentLocationDirLineEdit.setText(
            self.settingJsonService.get('attachment directory'))
        self.mainWindow.generalProcessExportFileDirLineEdit.setText(
            self.settingJsonService.get('export data file'))

        # 上次处理

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

        originalDataFile = self.exploreOriginalDataFile()

        if originalDataFile is None:
            return

        # 开始处理

        originalDataFrame = readIn(originalDataFile)

        originalDataFrame = self.preprocess.operate(originalDataFrame)
        originalDataFrame = self.process.operate(originalDataFrame)
        dataFrame = self.postprocess.operate(originalDataFrame)

        # ## 附件匹配

        shouldAttachmentMatch = True  # 是否要进行附件匹配的标志

        # 选取附件所在的文件夹

        attachmentDir = self.exploreAttachmentDirectory()

        if attachmentDir is None:

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

        exportDataFile = self.exploreExportDataFile()

        # 选择校验和文件格式校验

        if exportDataFile is None:

            self.informationMessage('未选择保存位置，本次结果未保存')

            return

        dataFrame.to_csv(exportDataFile, encoding="utf_8_sig", index=False)

        # ## 更新 settings.json 文件和处理成功

        self.updateSettingJsonUponProcessFinish(originalDataFrame, dataFrame)

        self.informationMessage('快速处理成功')

    def generalProcess(self):
        '''
        一般处理
        '''

        shouldAttachmentMatch = True  # 是否要进行附件匹配的标志

        # ## 目录读入和处理

        originalDataFile = self.mainWindow.generalProcessOriginalDataDirLineEdit.text()

        if originalDataFile == '':

            self.informationMessage('请设置原始记录文件')

            return

        attachmentDir = self.mainWindow.generalProcessAttachmentLocationDirLineEdit.text()

        if attachmentDir == '':

            self.informationMessage('未选择附件所在文件夹，本次结果将不进行附件匹配')

            shouldAttachmentMatch = False

        exportDataFile = self.mainWindow.generalProcessExportFileDirLineEdit.text()

        if exportDataFile is None:

            self.informationMessage('请选择保存位置')

            return

        # 开始处理

        originalDataFrame = readIn(originalDataFile)

        originalDataFrame = self.preprocess.operate(originalDataFrame)
        originalDataFrame = self.process.operate(originalDataFrame)
        dataFrame = self.postprocess.operate(originalDataFrame)

        # 附件匹配

        if shouldAttachmentMatch is True:

            dataFrame = self.attachmentMatch.operate(dataFrame, attachmentDir)

            attachmentDict = self.attachmentMatch.getHashDict()
            self.jsonService.save('attachment.json', attachmentDict)

            dataFrame = self.postprocess.reorderAfterAttachmentMatch(dataFrame)

        # 保存处理结果

        print(dataFrame.info())

        dataFrame.to_csv(exportDataFile, encoding="utf_8_sig", index=False)

        # 更新 settings.json 文件和处理成功

        self.updateSettingJsonUponProcessFinish(originalDataFrame, dataFrame)

        self.informationMessage('处理成功')

    def exploreOriginalDataFile(self) -> str:
        '''
        原始记录文件读入和校验

        返回值：
            - 文件通过校验
            originalDataFile (str): 文件路径和文件名

            - 文件未通过校验
            None
        '''

        # 选取原始记录文件
        originalDataFile, filetype = QtWidgets.QFileDialog.getOpenFileName(
            self.mainWindow, '选择原始记录文件', self.settingJsonService.get('original data file'), 'All Files (*.*);;CSV (Comma delimited) (*.csv)')

        # 选择校验
        if originalDataFile is None or originalDataFile == '':

            return None

        # 文件格式校验
        filetype = originalDataFile.split('.')[-1]

        if filetype.lower() != 'csv':

            self.informationMessage('文件格式错误，请选择 *.csv 格式的文件')

            return None

        # 更新 json 文件信息
        self.settingJsonService.set('original data file', originalDataFile)

        # 更新窗口显示信息
        self.mainWindow.generalProcessOriginalDataDirLineEdit.setText(
            originalDataFile)

        return originalDataFile

    def exploreAttachmentDirectory(self) -> str:
        '''
        附件所在目录读入和校验

        返回值：
            - 目录通过校验
            attachmentDir (str): 目录路径

            - 目录未通过校验
            None
        '''

        # 选取附件所在的文件夹
        attachmentDir = QtWidgets.QFileDialog.getExistingDirectory(
            self.mainWindow, '选取附件所在的文件夹', self.settingJsonService.get('attachment directory'))

        # 选择校验和文件格式校验
        if attachmentDir is None or attachmentDir == '':

            return None

        # 更新 json 文件信息
        self.settingJsonService.set('attachment directory', attachmentDir)

        # 更新窗口显示信息
        self.mainWindow.generalProcessAttachmentLocationDirLineEdit.setText(
            attachmentDir)

        return attachmentDir

    def exploreExportDataFile(self) -> str:
        '''
        导出处理结果记录文件读入和校验

        返回值：
            - 文件通过校验
            exportDataFile (str): 文件路径和文件名

            - 文件未通过校验
            None
        '''

        # 选取保存目录

        exportDataFile, filetype = QtWidgets.QFileDialog.getSaveFileName(
            self.mainWindow, '选择保存处理结果的目录', self.settingJsonService.get('export data file'), 'CSV (Comma delimited) (*.csv)')

        # 选择校验
        if exportDataFile is None or exportDataFile == '':

            return None

        # 更新 json 文件信息
        self.settingJsonService.set('export data file', exportDataFile)

        # 更新窗口显示信息
        self.mainWindow.generalProcessExportFileDirLineEdit.setText(
            exportDataFile)

        return exportDataFile

    def updateSettingJsonUponProcessFinish(self, originalDataFrame, dataFrame):
        '''
        处理结束后, 根据处理结果更新 settings.json 文件

        参数值：
            originalDataFrame (dataframe): process 后的 dataframe, 包含无问题记录
            dataFrame (dataframe): postprocess 后的 dataframe, 仅有效记录, 可能包含附件匹配记录
        '''

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

        # 更新 settings.json 文件, 上次处理
        self.settingJsonService.set('last process', thisProcessDetail)

        # 更新 settings.json 文件, 近期处理
        recentProcess = self.settingJsonService.get('recent process')
        recentProcess.append(thisProcessDetail)
        self.settingJsonService.set('recent process', recentProcess)

        # 从 settings.json 取值更新窗口
        self.updateWindowWithJson()
        self.mainWindow.lastProcessTitleLabel.setText('本次处理')


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
