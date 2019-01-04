# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'g:\pycharm\ChatBox\groupchatter.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(436, 348)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.info_textEdit = QtWidgets.QTextEdit(Form)
        self.info_textEdit.setObjectName("info_textEdit")
        self.gridLayout.addWidget(self.info_textEdit, 0, 0, 1, 1)
        self.send_textEdit = QtWidgets.QTextEdit(Form)
        self.send_textEdit.setObjectName("send_textEdit")
        self.gridLayout.addWidget(self.send_textEdit, 1, 0, 1, 1)
        self.send_btn = QtWidgets.QPushButton(Form)
        self.send_btn.setObjectName("send_btn")
        self.gridLayout.addWidget(self.send_btn, 2, 0, 1, 1)
        self.addMem_btn = QtWidgets.QPushButton(Form)
        self.addMem_btn.setObjectName("addMem_btn")
        self.gridLayout.addWidget(self.addMem_btn, 2, 1, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.gridLayout.addWidget(self.tableWidget, 0, 1, 2, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.send_btn.setText(_translate("Form", "Send"))
        self.addMem_btn.setText(_translate("Form", "Add Member"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "id"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "ip"))

