# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'g:\pycharm\ChatBox\pallist.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(388, 665)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/logo/app.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.add_Contact = QtWidgets.QPushButton(Form)
        self.add_Contact.setObjectName("add_Contact")
        self.gridLayout.addWidget(self.add_Contact, 4, 0, 1, 1)
        self.add_group = QtWidgets.QPushButton(Form)
        self.add_group.setObjectName("add_group")
        self.gridLayout.addWidget(self.add_group, 4, 1, 1, 1)
        self.treeWidget = QtWidgets.QTreeWidget(Form)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.treeWidget, 6, 0, 1, 2)
        self.palid_lineEdit = QtWidgets.QLineEdit(Form)
        self.palid_lineEdit.setObjectName("palid_lineEdit")
        self.gridLayout.addWidget(self.palid_lineEdit, 3, 0, 1, 1)
        self.quit_button = QtWidgets.QPushButton(Form)
        self.quit_button.setObjectName("quit_button")
        self.gridLayout.addWidget(self.quit_button, 7, 0, 1, 2)
        self.ip_Self = QtWidgets.QLabel(Form)
        self.ip_Self.setObjectName("ip_Self")
        self.gridLayout.addWidget(self.ip_Self, 2, 0, 1, 1)
        self.id_Self = QtWidgets.QLabel(Form)
        self.id_Self.setObjectName("id_Self")
        self.gridLayout.addWidget(self.id_Self, 1, 0, 1, 1)
        self.icon_Self = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.icon_Self.sizePolicy().hasHeightForWidth())
        self.icon_Self.setSizePolicy(sizePolicy)
        self.icon_Self.setMaximumSize(QtCore.QSize(90, 80))
        self.icon_Self.setText("")
        self.icon_Self.setPixmap(QtGui.QPixmap(":/logo/icon.jpg"))
        self.icon_Self.setScaledContents(True)
        self.icon_Self.setObjectName("icon_Self")
        self.gridLayout.addWidget(self.icon_Self, 1, 1, 3, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.add_Contact.setText(_translate("Form", "Add Pals"))
        self.add_group.setText(_translate("Form", "Add Group"))
        self.treeWidget.headerItem().setText(0, _translate("Form", "Friends"))
        self.quit_button.setText(_translate("Form", "Quit"))
        self.ip_Self.setText(_translate("Form", "IP:"))
        self.id_Self.setText(_translate("Form", "ID:"))

import chatbox_rc
