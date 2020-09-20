'''
主界面
'''

import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow

from Ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    '''
    主界面
    '''

    _padding = 10  # 边界宽度
    _topHeight = 80  # 上侧可拖动高度
    _leftHeight = 40  # 左侧可拖动宽度

    def __init__(self):
        '''
        初始化
        新建对象时默认执行
        '''

        # 初始化窗口
        QMainWindow.__init__(self)

        # 初始化 UI
        self.setupUi(self)

        # 一些可视化设置
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)  # 去掉标题栏
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 去掉边框
        self.setWindowOpacity(0.95)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        # 关闭和最小化按钮
        self.closeButton.pressed.connect(self.close)
        self.minimizeButton.pressed.connect(self.showMinimized)

        # 设置快捷键
        self.closeButton.setShortcut('Esc')

        # 设置鼠标跟踪判断标志默认值
        self._move_drag = False  # 移动
        self._corner_drag = False  # 右下拖动缩放
        self._bottom_drag = False  # 下侧拖动缩放
        self._right_drag = False  # 右侧拖动缩放

        # 读取 QSS 文件
        self.set_style('./MainWindowStyle.qss')

    def set_style(self, qssfile):
        '''
        读取外部 QSS 文件，并应用

        参数值：
            qssfile (str): 定位到 QSS 文件
        '''
        with open(qssfile, 'r') as qss:
            style = qss.read()  # 读取 QSS 文件内容
            self.setStyleSheet(style)  # 设置为样式表

    def resizeEvent(self, event):
        '''
        自定义窗口调整大小事件
        重新调整边界范围以备实现鼠标拖放缩放窗口大小，采用三个列表生成式生成三个列表
        '''

        # 右边界
        self._right_rect = [QtCore.QPoint(x, y)
                            for x in range(self.width() - self._padding, self.width() + 1)
                            for y in range(1, self.height() - self._padding)]
        # 下边界
        self._bottom_rect = [QtCore.QPoint(x, y)
                             for x in range(1, self.width() - self._padding)
                             for y in range(self.height() - self._padding, self.height() + 1)]
        # 右下角
        self._corner_rect = [QtCore.QPoint(x, y)
                             for x in range(self.width() - self._padding, self.width() + 1)
                             for y in range(self.height() - self._padding, self.height() + 1)]

    def mousePressEvent(self, event):
        '''
        自定义鼠标点击事件
        '''

        # 判断是否为鼠标左键点击，否则退出
        if event.button() != QtCore.Qt.LeftButton:
            return

        if event.pos() in self._corner_rect:
            # 右下角
            self._corner_drag = True
            event.accept()
        elif event.pos() in self._right_rect:
            # 右边界
            self._right_drag = True
            event.accept()
        elif event.pos() in self._bottom_rect:
            # 下边界
            self._bottom_drag = True
            event.accept()
        elif event.y() < self._topHeight:
            # 上标题区域
            self._move_drag = True
            self.move_DragPosition = event.globalPos() - self.pos()
            event.accept()
        elif event.x() < self._leftHeight:
            # 左标题区域
            self._move_drag = True
            self.move_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        '''
        自定义鼠标移动事件
        '''

        # 判断鼠标位置切换光标
        if event.pos() in self._corner_rect:
            # 右下角
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif event.pos() in self._right_rect:
            # 右边界
            self.setCursor(QtCore.Qt.SizeHorCursor)
        elif event.pos() in self._bottom_rect:
            # 下边界
            self.setCursor(QtCore.Qt.SizeVerCursor)
        else:
            self.setCursor(QtCore.Qt.ArrowCursor)

        # 当鼠标左键点击不放及满足点击区域的要求后，分别实现不同的窗口调整
        if QtCore.Qt.LeftButton and self._right_drag:
            # 右侧调整窗口宽度
            self.resize(event.pos().x(), self.height())
            event.accept()
        elif QtCore.Qt.LeftButton and self._bottom_drag:
            # 下侧调整窗口高度
            self.resize(self.width(), event.pos().y())
            event.accept()
        elif QtCore.Qt.LeftButton and self._corner_drag:
            # 右下角同时调整高度和宽度
            self.resize(event.pos().x(), event.pos().y())
            event.accept()
        elif QtCore.Qt.LeftButton and self._move_drag:
            # 标题区域移动窗口
            self.move(event.globalPos() - self.move_DragPosition)
            event.accept()

    def mouseReleaseEvent(self, event):
        '''
        自定义鼠标释放事件
        '''

        # 将光标恢复为箭头
        self.setCursor(QtCore.Qt.ArrowCursor)

        # 各标志复位
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False

    def closeEvent(self, event):
        '''
        自定义关闭窗口事件
        重写该方法主要为了解决关闭主窗口但子窗口仍显示的问题
        使用 sys.exit(0) 时就会只要关闭了主窗口，所有关联的子窗口也会全部关闭
        '''

        sys.exit(0)


if __name__ == '__main__':
    # 执行入口

    # 设置高分辨率屏幕行为
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.AA_EnableHighDpiScaling)  # 支持高分辨率屏幕
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.AA_UseHighDpiPixmaps)  # 使用高分辨率图标

    # 程序载入
    app = QtWidgets.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
