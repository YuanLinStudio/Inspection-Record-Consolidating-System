import sys

import numpy
import pandas
from PyQt5 import QtCore, QtGui, QtWidgets

from AttachmentMatch import AttachmentMatch
from JsonService import saveJson
from Postprocess import Postprocess
from Preprocess import Preprocess
from Process import Process
from readIn import readIn


class WindowController:

    def __init__(self):

        # 主窗口
        self.mainWindow = MainWindow()

        # 服务项
        self.preprocess = Preprocess()
        self.process = Process()
        self.postprocess = Postprocess()
        self.attachmentMatch = AttachmentMatch()

    def show(self):
        pass


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
