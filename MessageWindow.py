'''
信息提示界面
'''

import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class MessageWindow(QtWidgets.QWidget):
    '''
    信息提示界面
    '''

    def __init__(self, message=''):

        # 初始化窗口
        super().__init__()

        # 设置窗口内容
        self.setObjectName("messageWindow")
        self.setWindowTitle('信息')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('./images/index.png'),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName("mainLayout")

        self.topWidget = QtWidgets.QWidget(self)
        self.topWidget.setObjectName("topWidget")
        self.topWidget.setMaximumHeight(20)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.topWidget)
        self.horizontalLayout.setContentsMargins(10, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.titleLabel = QtWidgets.QLabel(self.topWidget)
        self.titleLabel.setText("")
        self.horizontalLayout.addWidget(self.titleLabel)

        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.closeButton = QtWidgets.QPushButton(self.topWidget)
        self.closeButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap('./images/close.png'),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(icon1)
        self.closeButton.setIconSize(QtCore.QSize(10, 10))
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.mainLayout.addWidget(self.topWidget)

        self.messageWidget = QtWidgets.QWidget(self)
        self.messageWidget.setObjectName("messageWidget")
        self.messageLayout = QtWidgets.QVBoxLayout(self.messageWidget)
        self.messageLayout.setContentsMargins(10, 10, 10, 10)
        self.messageLayout.setSpacing(0)
        self.messageLayout.setObjectName("messageLayout")
        self.messageLabel = QtWidgets.QLabel(self.messageWidget)
        self.messageLabel.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.messageLabel.setObjectName("messageLabel")
        self.messageLabel.setText(message)
        self.messageLayout.addWidget(self.messageLabel)
        self.mainLayout.addWidget(self.messageWidget)

        # 一些可视化设置
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)  # 去掉标题栏
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 去掉边框
        self.setWindowOpacity(0.95)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        # 关闭按钮
        self.closeButton.pressed.connect(self.close)

        # 设置快捷键
        self.closeButton.setShortcut('Esc')

        # 设置自动关闭
        self.setAutoClose(False)

        # 设置鼠标跟踪判断标志默认值
        self._move_drag = False  # 移动

        # 读取 QSS 文件
        self.set_style('./MessageWindowStyle.qss')

    def setAutoClose(self, countdown=3):
        '''
        设置自动关闭

        参数值：
            countdown (int): 从开启到自动关闭的时间
        '''
        
        # 定时关闭
        self.timer = QtCore.QTimer()
        
        if countdown is not False:
            self.timer.setInterval(countdown * 1000)
            self.timer.timeout.connect(self.close)

    def setMessage(self, message):
        '''
        设置信息内容

        参数值：
            message (str): 信息内容
        '''
        self.messageLabel.setText(message)

    def setTitle(self, title):
        '''
        设置窗口标题

        参数值：
            title (str): 标题内容
        '''
        self.titleLabel.setText(title)
        self.setWindowTitle(title)
    
    def showEvent(self, event):
        '''
        自定义显示窗口事件
        '''
        self.timer.start()
        event.accept()

    def closeEvent(self, event):
        '''
        自定义关闭窗口事件
        '''
        self.timer.stop()
        event.accept()

    def set_style(self, qssfile):
        '''
        读取外部 QSS 文件，并应用

        参数值：
            qssfile (str): 定位到 QSS 文件
        '''
        with open(qssfile, 'r') as qss:
            style = qss.read()  # 读取 QSS 文件内容
            self.setStyleSheet(style)  # 设置为样式表

    def mousePressEvent(self, event):
        '''
        自定义鼠标点击事件
        '''

        # 判断是否为鼠标左键点击，否则退出
        if event.button() != QtCore.Qt.LeftButton:
            return

        self.timer.stop()

        self._move_drag = True
        self.move_DragPosition = event.globalPos() - self.pos()
        event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        '''
        自定义鼠标移动事件
        '''

        # 当鼠标左键点击不放及满足点击区域的要求后，分别实现不同的窗口调整
        if QtCore.Qt.LeftButton and self._move_drag:
            # 标题区域移动窗口
            self.move(QMouseEvent.globalPos() - self.move_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        '''
        自定义鼠标释放事件
        '''

        # 各标志复位
        self._move_drag = False


if __name__ == '__main__':
    # 执行入口

    # 设置高分辨率屏幕行为
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.AA_EnableHighDpiScaling)  # 支持高分辨率屏幕
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.AA_UseHighDpiPixmaps)  # 使用高分辨率图标

    # 程序载入
    app = QtWidgets.QApplication(sys.argv)
    widget = MessageWindow()
    widget.show()
    sys.exit(app.exec_())
