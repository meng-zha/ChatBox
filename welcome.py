# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'welcome.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.login_button = QtWidgets.QPushButton(self.centralwidget)
        self.login_button.setGeometry(QtCore.QRect(330, 350, 131, 51))
        self.login_button.setObjectName("login_button")
        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(330, 420, 131, 51))
        self.exit_button.setObjectName("exit_button")
        self.username_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.username_lineEdit.setGeometry(QtCore.QRect(370, 150, 181, 51))
        self.username_lineEdit.setObjectName("username_lineEdit")
        self.password_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.password_lineEdit.setGeometry(QtCore.QRect(370, 230, 181, 51))
        self.password_lineEdit.setObjectName("password_lineEdit")
        self.username_label = QtWidgets.QLabel(self.centralwidget)
        self.username_label.setGeometry(QtCore.QRect(270, 160, 71, 31))
        self.username_label.setObjectName("username_label")
        self.password_label = QtWidgets.QLabel(self.centralwidget)
        self.password_label.setGeometry(QtCore.QRect(270, 240, 71, 31))
        self.password_label.setObjectName("password_label")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(180, 15, 471, 91))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.exit_button.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.login_button.setText(_translate("MainWindow", "LOGIN"))
        self.exit_button.setText(_translate("MainWindow", "EXIT"))
        self.username_label.setText(_translate("MainWindow", "Username"))
        self.password_label.setText(_translate("MainWindow", "Password"))
        self.label.setText(_translate("MainWindow", "P2P Chat"))

