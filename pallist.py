# -*- coding: utf-8 -*-

import random
import re
from socket import *

import PyQt5.QtCore as PQC
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem, QWidget, QMenu, QAction, QInputDialog

from static_var import *
from Ui_pallist import Ui_Form
import chatting


class PalList(QWidget):
    logout_signal = PQC.pyqtSignal()
    refresh_sigal = PQC.pyqtSignal()
    # grouplist = []

    def __init__(self, *args):
        super(PalList, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.username = args[0]
        self.ip = args[1]
        self.ui.id_Self.setText('id:   ' + self.username)
        self.ui.ip_Self.setText('ip:   ' + self.ip)
        self.ui.palid_lineEdit.setText('2015011463')
        self.grouplist = []
        self.chatters = []
        self.root = self.creategroup('My Friends')
        self.root.setExpanded(True)
        self.ui.treeWidget.setContextMenuPolicy(PQC.Qt.CustomContextMenu)
        self.ui.treeWidget.customContextMenuRequested[PQC.QPoint].connect(self.contextMenuEvent) 

        self.ui.add_Contact.clicked.connect(self.add_Pal)
        self.ui.quit_button.clicked.connect(self.logout)
        self.refresh_sigal.connect(self.refresh)
        self.ui.treeWidget.itemDoubleClicked.connect(self.chatbox)

    def add_Pal(self):
        pal_id = self.ui.palid_lineEdit.text()
        if (re.match(r'201\d{7}', pal_id)):
            consult = socket(AF_INET, SOCK_STREAM)
            consult.connect(ADDR)
            consult.send(('q' + pal_id).encode())

            data = consult.recv(BUFSIZ).decode('utf-8')
            if data == 'Incorrect No.' or data == 'Please send the correct message.':
                QMessageBox.information(self, "Warning", data)
            else:
                child = QTreeWidgetItem()
                child.setText(0, 'id:' + pal_id + ' ip:' + data)
                self.root.addChild(child)
                self.grouplist[0]['pal_count'] += 1
                if data != 'n':
                    self.grouplist[0]['pal_online'] += 1
                self.refresh_sigal.emit()
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
        group = QTreeWidgetItem(self.ui.treeWidget)
        groupdic = {
            'group': group,
            'group_name': groupname,
            'pal_count': 0,
            'pal_online': 0
        }
        self.grouplist.append(groupdic)

        groupname += ' ' + str(groupdic['pal_online']) + '/' + str(
            groupdic['pal_count'])
        group.setText(0, groupname)
        return group

    def refresh(self):
        for i in range(len(self.grouplist)):
            groupdic = self.grouplist[i]
            groupname = groupdic['group_name'] + ' ' + str(
                groupdic['pal_online']) + '/' + str(groupdic['pal_count'])
            self.ui.treeWidget.topLevelItem(i).setText(0, groupname)

    def search(self,id):
        for i in self.grouplist:
            if id == i['group_name']:
                return True

        # TODO:需要继续写好友的查询

    def chatbox(self):
        if self.ui.treeWidget.currentItem().parent() is not None:
            chatter = chatting.Chatting(self.username, self.ip, self.ui.treeWidget.currentItem().text(0))
            chatter.show()
            self.chatters.append(chatter)

    def contextMenuEvent(self, event):
        pmenu = QMenu(self)
        pcontact = QAction('Add Group',self.ui.treeWidget)
        pcontact.triggered.connect(lambda:self.inputDialog(0))
        pmenu.addAction(pcontact)
        pmenu.exec_(QtGui.QCursor.pos())

    def inputDialog(self,flag):
        if flag == 0:
            # add contact group
            text, ok = QInputDialog.getText(self, 'Input', 'Group Name:')
            if ok:
                self.creategroup(text)
