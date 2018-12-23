# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget,QMessageBox,QTreeWidgetItem
from socket import *
import re
import PyQt5.QtCore as PQC
import random

from static_var import *
from Ui_pallist import Ui_Form

class PalList(QWidget):
    logout_signal= PQC.pyqtSignal()

    def __init__(self, *args):
        super(PalList, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.username = args[0]
        self.ip = args[1]
        self.ui.id_Self.setText('id:   '+self.username)
        self.ui.ip_Self.setText('ip:   '+self.ip)
        self.root = self.creategroup('My Friends')
        self.root.setExpanded(True)

        self.ui.add_Contact.clicked.connect(self.add_Pal)
        self.ui.quit_button.clicked.connect(self.logout)

    def add_Pal(self):
        pal_id = self.ui.palid_lineEdit.text()
        if(re.match('201\d{7}',pal_id)):
            consult = socket(AF_INET, SOCK_STREAM)
            consult.connect(ADDR)
            consult.send(('q'+pal_id).encode())

            data = consult.recv(BUFSIZ).decode('utf-8')
            if data == 'Incorrect No.' or data == 'Please send the correct message.':
                QMessageBox.information(self, "Warning", data)
            else:
                child = QTreeWidgetItem()
                child.setText(0,'id:'+pal_id+' ip:'+data)
                self.root.addChild(child)
        else:
            QMessageBox.information(self, "Warning", "Illegal Username!")

    def logout(self):
        request = socket(AF_INET, SOCK_STREAM)
        request.connect(ADDR)
        request.send(('logout' + self.username).encode())

        data = request.recv(BUFSIZ).decode('utf-8')
        if data == 'loo':
            self.logout_signal.emit()
        else:
            QMessageBox.information(self, "Warning", 'Logout failed')

    def creategroup(self, groupname):
        hidernum = 0
        group = QTreeWidgetItem(self.ui.treeWidget)
        groupdic = {'group': group, 'group_name': groupname, 'pal_count': 0, 'pal_online': 0}

        groupname += ' ' + str(groupdic['pal_online']) + '/' + str(groupdic['pal_count'])
        group.setText(0, groupname)
        return group
