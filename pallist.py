# -*- coding: utf-8 -*-

import random
import re
import time
import threading
from socket import *

import PyQt5.QtCore as PQC
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem, QWidget, QMenu, QAction, QInputDialog

from static_var import *
from Ui_pallist import Ui_Form
import chatting


class PalList(QWidget):
    logout_signal = PQC.pyqtSignal()
    refresh_signal = PQC.pyqtSignal()

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
        self.grouplist = []  # 存储分组信息
        self.contactlist = []  #存储好友信息
        self.chatterlist = []  #存储聊天框
        self.root = self.creategroup('My Friends')
        self.root.setExpanded(True)

        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.threadsocket = threading.Thread(target=self.initserver,name='welcome')
        self.threadsocket.start()

        # 分组右键菜单
        self.ui.treeWidget.setContextMenuPolicy(PQC.Qt.CustomContextMenu)
        self.ui.treeWidget.customContextMenuRequested[PQC.QPoint].connect(
            self.contextMenuEvent)

        self.ui.add_Contact.clicked.connect(self.add_Pal)
        self.ui.quit_button.clicked.connect(self.logout)
        self.refresh_signal.connect(self.refresh)
        self.ui.treeWidget.itemDoubleClicked.connect(self.chatbox)

    def initserver(self):
        self.serverSocket.bind((self.ip, CHAT_PORT))
        self.serverSocket.listen(10)
        while(True):
            try:
                clientSocket,clientInfo = self.serverSocket.accept()
                index = self.search_ip(clientInfo)
                listenThread = threading.Thread(target=self.chatterlist[index].recvMessage,args=(clientSocket,),name='listen')
                listenThread.start()
            except Exception:
                break

    def add_Pal(self):
        pal_id = self.ui.palid_lineEdit.text()
        if re.match(r'201\d{7}', pal_id):
            consult = socket(AF_INET, SOCK_STREAM)
            consult.connect(ADDR)
            consult.send(('q' + pal_id).encode())

            data = consult.recv(BUFSIZ).decode('utf-8')
            if data == 'Incorrect No.' or data == 'Please send the correct message.':
                QMessageBox.information(self, "Warning", data)
            else:
                if self.search(pal_id) >= -1:
                    QMessageBox.information(self, "Warning", 'Contact Existed')
                else:
                    child = QTreeWidgetItem()
                    child.setText(0, 'id:' + pal_id + ' ip:' + data)
                    self.root.addChild(child)
                    contactdic = {
                        'contact': child,
                        'group_index': 0,
                        'contact_id': pal_id,
                        'contact_ip': data,
                        'online': False
                    }
                    self.grouplist[0]['pal_count'] += 1
                    if data != 'n':
                        self.grouplist[0]['pal_online'] += 1
                        contactdic['online'] = True
                    self.contactlist.append(contactdic)
                    self.chatterlist.append(None)
                    self.refresh_signal.emit()
        else:
            QMessageBox.information(self, "Warning", "Illegal Username!")

    def __del__(self):
        del self.serverSocket

    def logout(self):
        request = socket(AF_INET, SOCK_STREAM)
        request.connect(ADDR)
        request.send(('logout' + self.username).encode())

        data = request.recv(BUFSIZ).decode('utf-8')
        if data == 'loo':
            self.serverSocket.close()
            for i in self.chatterlist:
                if i is not None:
                    i.close()
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
            groupdic['group'].setText(0, groupname)

    def search(self, key):
        for i, k in enumerate(self.grouplist):
            if key == k['group_name']:
                return i
        # if key == self.username:
        #     return -1
        for i, k in enumerate(self.contactlist):
            if key == k['contact_id']:
                return i
        return -2

    def search_item(self,key):
        for i, k in enumerate(self.contactlist):
            if key == k['contact_ip']:
                return i
        return -1

    def search_ip(self,key):
        for i, k in enumerate(self.contactlist):
            if key == k['contact']:
                return i
        return -1

    def chatbox(self):
        selectItem = self.ui.treeWidget.currentItem()
        if self.ui.treeWidget.currentItem().parent() is not None:
            index = self.search_item(selectItem)
            chatter = chatting.Chatting(
                self.username, self.ip,
                self.contactlist[index])
            chatter.show()
            self.chatterlist[index]=chatter

    def contextMenuEvent(self):
        selectitem = self.ui.treeWidget.currentItem()
        if selectitem:
            if selectitem.parent() is None:
                Menu = QMenu(self)
                AddGroupAct = QAction('Add Group', self.ui.treeWidget)
                AddGroupAct.triggered.connect(lambda: self.inputDialog(0))
                Menu.addAction(AddGroupAct)
                if selectitem is not self.root:
                    DeleteGroupAct = QAction('Delete Group',
                                             self.ui.treeWidget)
                    DeleteGroupAct.triggered.connect(self.deleteGroup)
                    Menu.addAction(DeleteGroupAct)
                Menu.exec_(QtGui.QCursor.pos())
            else:
                Menu = QMenu(self)
                DeleteAct = QAction('Delete', Menu)
                Menu.addAction(DeleteAct)
                DeleteAct.triggered.connect(self.deleteContact)
                if len(self.grouplist) > 1:
                    SubMenu = QMenu('Transfer to', Menu)
                    Menu.addMenu(SubMenu)
                    for group_dic in self.grouplist:
                        if group_dic['group'] is not selectitem.parent():
                            MoveAct = QAction(group_dic['group_name'], Menu)
                            SubMenu.addAction(MoveAct)
                            MoveAct.triggered.connect(self.moveContact)
                Menu.exec_(QtGui.QCursor.pos())

    def deleteGroup(self):
        selectItem = self.ui.treeWidget.currentItem()
        index = self.ui.treeWidget.indexOfTopLevelItem(selectItem)
        for k, i in enumerate(self.grouplist):
            if i['group'] is selectItem:
                self.root.addChildren(selectItem.takeChildren())
                self.grouplist[0]['pal_count'] += i['pal_count']
                self.grouplist[0]['pal_online'] += i['pal_online']
                for j in self.contactlist:
                    if j['group_index'] == k:
                        j['group_index'] = 0
                self.ui.treeWidget.takeTopLevelItem(index)
                self.grouplist.remove(i)
        self.refresh_signal.emit()

    def deleteContact(self):
        selectItem = self.ui.treeWidget.currentItem()
        for i in self.contactlist:
            if i['contact'] is selectItem:
                self.grouplist[i['group_index']]['pal_count'] -= 1
                if i['online'] is True:
                    self.grouplist[i['group_index']]['pal_online'] -= 1
                index = selectItem.parent().indexOfChild(selectItem)
                selectItem.parent().takeChild(index)
                self.contactlist.remove(i)
        self.refresh_signal.emit()

    def moveContact(self):
        selectItem = self.ui.treeWidget.currentItem()
        group_name = self.sender().text()
        indexTo = self.search(group_name)
        for i in self.contactlist:
            if i['contact'] is selectItem:
                selectItem.parent().removeChild(selectItem)
                self.grouplist[indexTo]['group'].addChild(selectItem)
                self.grouplist[i['group_index']]['pal_count'] -= 1
                self.grouplist[indexTo]['pal_count'] += 1
                if i['online'] is True:
                    self.grouplist[i['group_index']]['pal_online'] -= 1
                    self.grouplist[indexTo]['pal_online'] += 1
                i['group_index'] = indexTo
        self.refresh_signal.emit()

    def inputDialog(self, flag):
        if flag == 0:
            # add contact group
            text, ok = QInputDialog.getText(self, 'Input', 'Group Name:')
            if ok:
                if self.search(text) >= 0:
                    QMessageBox.information(self, "Warning", 'Name Existed')
                else:
                    self.creategroup(text)
