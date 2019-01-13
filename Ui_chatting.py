# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'g:\pycharm\ChatBox\chatting.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Chatting(object):
    def setupUi(self, Chatting):
        Chatting.setObjectName("Chatting")
        Chatting.resize(629, 525)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/logo/app.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Chatting.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Chatting)
        self.gridLayout.setObjectName("gridLayout")
        self.emoji_table = QtWidgets.QTableWidget(Chatting)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.emoji_table.sizePolicy().hasHeightForWidth())
        self.emoji_table.setSizePolicy(sizePolicy)
        self.emoji_table.setMinimumSize(QtCore.QSize(200, 0))
        self.emoji_table.setMaximumSize(QtCore.QSize(200, 16777215))
        self.emoji_table.setObjectName("emoji_table")
        self.emoji_table.setColumnCount(0)
        self.emoji_table.setRowCount(0)
        self.gridLayout.addWidget(self.emoji_table, 0, 3, 3, 1)
        self.send_textEdit = QtWidgets.QTextEdit(Chatting)
        self.send_textEdit.setObjectName("send_textEdit")
        self.gridLayout.addWidget(self.send_textEdit, 1, 0, 1, 3)
        self.send_pushButton = QtWidgets.QPushButton(Chatting)
        self.send_pushButton.setObjectName("send_pushButton")
        self.gridLayout.addWidget(self.send_pushButton, 2, 2, 1, 1)
        self.files_pushButton = QtWidgets.QPushButton(Chatting)
        self.files_pushButton.setObjectName("files_pushButton")
        self.gridLayout.addWidget(self.files_pushButton, 2, 1, 1, 1)
        self.record_btn = QtWidgets.QPushButton(Chatting)
        self.record_btn.setObjectName("record_btn")
        self.gridLayout.addWidget(self.record_btn, 2, 0, 1, 1)
        self.info_display = QtWidgets.QTextEdit(Chatting)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.info_display.sizePolicy().hasHeightForWidth())
        self.info_display.setSizePolicy(sizePolicy)
        self.info_display.setMinimumSize(QtCore.QSize(400, 300))
        self.info_display.setReadOnly(True)
        self.info_display.setObjectName("info_display")
        self.gridLayout.addWidget(self.info_display, 0, 0, 1, 3)

        self.retranslateUi(Chatting)
        QtCore.QMetaObject.connectSlotsByName(Chatting)

    def retranslateUi(self, Chatting):
        _translate = QtCore.QCoreApplication.translate
        Chatting.setWindowTitle(_translate("Chatting", "Form"))
        self.send_pushButton.setText(_translate("Chatting", "Send"))
        self.files_pushButton.setText(_translate("Chatting", "Files"))
        self.record_btn.setText(_translate("Chatting", "Record"))

import chatbox_rc
