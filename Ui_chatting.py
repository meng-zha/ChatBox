# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'g:\pycharm\ChatBox\chatting.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(552, 413)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.files_pushButton = QtWidgets.QPushButton(Form)
        self.files_pushButton.setObjectName("files_pushButton")
        self.gridLayout.addWidget(self.files_pushButton, 2, 0, 1, 1)
        self.info_display = QtWidgets.QTextEdit(Form)
        self.info_display.setReadOnly(True)
        self.info_display.setObjectName("info_display")
        self.gridLayout.addWidget(self.info_display, 0, 0, 1, 2)
        self.send_pushButton = QtWidgets.QPushButton(Form)
        self.send_pushButton.setObjectName("send_pushButton")
        self.gridLayout.addWidget(self.send_pushButton, 2, 1, 1, 1)
        self.send_textEdit = QtWidgets.QTextEdit(Form)
        self.send_textEdit.setObjectName("send_textEdit")
        self.gridLayout.addWidget(self.send_textEdit, 1, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.files_pushButton.setText(_translate("Form", "Files"))
        self.send_pushButton.setText(_translate("Form", "Send"))

