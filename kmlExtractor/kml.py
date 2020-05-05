# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'kml.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import kmlCoordExtractor
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(242, 111)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 30, 158, 25))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 242, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        abAction=QAction('关于',self)

        self.menubar.addAction(abAction)
        abAction.triggered.connect(self.showAbout)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.filename=None

        self.setWindowTitle('KML EXTRACTOE')
        self.pushButton.clicked.connect(self.openFile)
        self.pushButton_2.clicked.connect(self.extract)

    def showAbout(self):
        QMessageBox.about(self, '关于', r'更多见https://zhuanlan.zhihu.com/c_1239206955782107136，欢迎关注知乎专栏：写代码的攻城狮')
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "打开kml文件"))
        self.pushButton_2.setText(_translate("MainWindow", "提取坐标"))
        self.menu.setTitle(_translate("MainWindow", "关于..."))

    def openFile(self):
        filename=QFileDialog.getOpenFileName(self,'选择文件','','KML文件(*.kml)')
        self.filename=filename[0]

    def extract(self):
        if not self.filename:
            QMessageBox.about(self,'错误','重新选择kml文件')
            return None
        else:
            print(self.filename)
            kmlCoordExtractor.Kce(self.filename)
            QMessageBox.about(self, '成功', '提取成功')




