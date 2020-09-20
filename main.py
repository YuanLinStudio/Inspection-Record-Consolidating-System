'''
主程序启动器
'''

import sys

from PyQt5 import QtCore, QtWidgets

from WindowController import WindowController

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
