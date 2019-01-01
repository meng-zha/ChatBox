# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'g:\pycharm\ChatBox\sendfile.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SendFile(object):
    def setupUi(self, SendFile):
        SendFile.setObjectName("SendFile")
        SendFile.resize(404, 256)
        self.layoutWidget = QtWidgets.QWidget(SendFile)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 40, 361, 191))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.filename_label = QtWidgets.QLabel(self.layoutWidget)
        self.filename_label.setText("")
        self.filename_label.setObjectName("filename_label")
        self.verticalLayout.addWidget(self.filename_label)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.progressBar = QtWidgets.QProgressBar(self.layoutWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ok_pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.ok_pushButton.setObjectName("ok_pushButton")
        self.horizontalLayout.addWidget(self.ok_pushButton)
        self.reject_pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.reject_pushButton.setObjectName("reject_pushButton")
        self.horizontalLayout.addWidget(self.reject_pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(SendFile)
        QtCore.QMetaObject.connectSlotsByName(SendFile)

    def retranslateUi(self, SendFile):
        _translate = QtCore.QCoreApplication.translate
        SendFile.setWindowTitle(_translate("SendFile", "Dialog"))
        self.label.setText(_translate("SendFile", "File To Send:"))
        self.ok_pushButton.setText(_translate("SendFile", "OK"))
        self.reject_pushButton.setText(_translate("SendFile", "Cancel"))

