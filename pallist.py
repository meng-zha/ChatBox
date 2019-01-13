# -*- coding: utf-8 -*-

import random
import re
import os
import time
import codecs
import pickle
import threading
from socket import *

import PyQt5.QtCore as PQC
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem, QWidget, QMenu, QAction, QInputDialog

from static_var import *
from Ui_pallist import Ui_Form
import chatting
import groupchatter
import multicastAddress


class PalList(QWidget):
    logout_signal = PQC.pyqtSignal()
    refresh_signal = PQC.pyqtSignal()
    dealadd_signal = PQC.pyqtSignal(str)

    def __init__(self, *args):
        super(PalList, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.isExisted = True
        self.setWindowTitle('ChatBox')

        self.path='./{}/'.format(args[0])
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.username = args[0]
        self.ip = args[1]
        self.ui.id_Self.setText('id:   ' + self.username)
        self.ui.ip_Self.setText('ip:   ' + self.ip)
        self.ui.palid_lineEdit.setText('')
        self.grouplist = []  # 存储分组信息
        self.contactlist = []  #存储好友信息
        self.chatterlist = []  #存储聊天框
        self.gchatterlist = []  #存储群聊框
        self.waitAdd=[] #待处理好友请求
        self.root = self.creategroup('My Friends')
        self.root.setExpanded(True)

        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.threadsocket = threading.Thread(
            target=self.initserver, name='welcome')
        self.threadsocket.start()

        self.addPalSocket = socket(AF_INET, SOCK_STREAM)
        self.threadaddPal = threading.Thread(
            target=self.initaddPalServer, name='addPal')
        self.threadaddPal.start()

        self.refreshThread = threading.Thread(target = self.timeRefresh,name='refresh')
        self.refreshThread.start()

        # 分组右键菜单
        self.ui.treeWidget.setContextMenuPolicy(PQC.Qt.CustomContextMenu)
        self.ui.treeWidget.customContextMenuRequested[PQC.QPoint].connect(
            self.contextMenuEvent)

        self.ui.add_Contact.clicked.connect(self.add_Pal)
        self.ui.add_group.clicked.connect(lambda: self.inputDialog(1))
        self.ui.quit_button.clicked.connect(self.close)
        self.refresh_signal.connect(self.refresh)
        self.ui.treeWidget.itemDoubleClicked.connect(self.chatbox)
        self.dealadd_signal.connect(self.dealaddPal)

        self.initContactList()

    def initserver(self):
        self.serverSocket.bind((self.ip, CHAT_PORT))
        self.serverSocket.listen(10)
        while (True):
            try:
                clientSocket, clientInfo = self.serverSocket.accept()
                index, flag = self.search_ip(clientInfo[0])
                if flag == 0:
                    listenThread = threading.Thread(
                        target=self.chatterlist[index].recvMessage,
                        args=(clientSocket, ),
                        name='listen')
                listenThread.start()
            except Exception:
                break

    def initaddPalServer(self):
        self.addPalSocket.bind((self.ip, APPLY_PORT))
        self.addPalSocket.listen(10)
        while (True):
            try:
                clientSocket, clientInfo = self.addPalSocket.accept()
                recvData = clientSocket.recv(BUFSIZ)
                clientSocket.close()
                if recvData:
                    self.dealadd_signal.emit(recvData.decode())
            except Exception:
                break

    def initContactList(self):
        if os.path.exists(self.path + 'contact.txt') and os.path.getsize(self.path + 'contact.txt') > 0:
            contactStFile = open(self.path + 'contact.txt', 'rb')
            store_data=contactStFile.read()
            contactStFile.close()
            store = pickle.loads(store_data)
            store_contact = store['contact']
            store_group = store['group']
            for i in store_group:
                self.creategroup(i['group_name'])
            for i in store_contact:
                self.added_friend(i['contact_id'],i['contact_ip'],i['group_index'])
                if i['contact_ip'] == 'n':
                    self.contactlist[-1]['online']=False
                    self.grouplist[i['group_index']]['pal_online']-=1
                self.refresh_signal.emit()

    def timeRefresh(self):
        while(self.isExisted):
            self.consult_all()
            time.sleep(5)

    def dealaddPal(self, message):
        info = message.split('_')
        connect = socket(AF_INET, SOCK_STREAM)
        connect.settimeout(1)
        connect.connect((info[2], APPLY_PORT))
        if info[0] == 'query':
            if info[1] in self.waitAdd:
                connect.close()
                return
            self.waitAdd.append(info[1])
            isrecv = QMessageBox.information(
                self,
                "query for receive", 'query of add pal from {} {}'.format(
                    info[1], info[2]), QMessageBox.Yes, QMessageBox.No)
            if isrecv == QMessageBox.Yes:
                self.added_friend(info[1], info[2],0)
                connect.send('ok_{}_{}'.format(self.username,
                                               self.ip).encode())
            else:
                connect.send('refuse_{}_{}'.format(self.username,
                                                   self.ip).encode())
        if info[0] == 'ok':
            self.added_friend(info[1], info[2],0)
        if info[0] == 'refuse':
            QMessageBox.information(self, "Warning", 'The request is refused!')

        connect.close()

    def add_Pal(self):
        pal_id = self.ui.palid_lineEdit.text()
        if re.match(r'201\d{7}', pal_id):
            consult = socket(AF_INET, SOCK_STREAM)
            consult.settimeout(1)
            try:
                consult.connect(ADDR)
                consult.send(('q' + pal_id).encode())
            except:
                print('Connect Server Exception!')
                consult.close()
                return

            data = consult.recv(BUFSIZ).decode('utf-8')
            consult.close()
            if data == 'Incorrect No.' or data == 'Please send the correct message.':
                QMessageBox.information(self, "Warning", data)
            else:
                if self.search(pal_id) >= -1:
                    QMessageBox.information(self, "Warning", 'Contact Existed')
                else:
                    if data == 'n':
                        QMessageBox.information(self, "Warning", 'Not online')
                    else:
                        connect = socket(AF_INET, SOCK_STREAM)
                        connect.settimeout(1)
                        try:
                            connect.connect((data, APPLY_PORT))
                            connect.send('query_{}_{}'.format(
                                self.username, self.ip).encode())
                        except:
                            QMessageBox.information(self, "Warning", 'Time Out')
                            connect.close()
                        connect.close()
        else:
            QMessageBox.information(self, "Warning", "Illegal Username!")

    def added_friend(self, pal_id, pal_ip,group_index):
        if self.search(pal_id) < 0:
            child = QTreeWidgetItem()
            child.setText(0, 'id:' + pal_id + ' ip:' + pal_ip)
            self.grouplist[group_index]['group'].addChild(child)
            contactdic = {
                'contact': child,
                'group_index': group_index,
                'contact_id': pal_id,
                'contact_ip': pal_ip,
                'online': True
            }
            self.grouplist[group_index]['pal_count'] += 1
            self.grouplist[group_index]['pal_online'] += 1
            self.contactlist.append(contactdic)
            chatter = chatting.Chatting(self.username, self.ip, contactdic)
            chatter.createMulticast_signal.connect(self.joinGchatter)
            chatter.newsform_signal.connect(self.newsform)
            self.chatterlist.append(chatter)
            self.refresh_signal.emit()

    def newsform(self,id):
        # 新消息提示
        index = self.search(id)
        if index >=0 :
            text = self.contactlist[index]['contact'].text(0)
            sptext = text.split('\n ')
            if len(sptext)==1:
                self.contactlist[index]['contact'].setText(0,text+'\n new message!')

    def __del__(self):
        del self.serverSocket

    def logout(self):
        request = socket(AF_INET, SOCK_STREAM)
        request.settimeout(1)
        try:
            request.connect(ADDR)
            request.send(('logout' + self.username).encode())

            data = request.recv(BUFSIZ).decode('utf-8')
        except:
            data = ''
            
        if data != 'loo':
            QMessageBox.information(self, "Warning", 'Logout failed')

        store_contact = [{'contact_id':i['contact_id'],'contact_ip':i['contact_ip'],'group_index':i['group_index']} for i in self.contactlist]
        store_group = [{'group_name':j['group_name'],'index':i} for i,j in enumerate(self.grouplist)]
        store_group = store_group[1:]   # 去除我的好友，有默认创建  
        store = {'contact':store_contact,'group':store_group}
        store_data = pickle.dumps(store)
        contactStFile = open(self.path+'contact.txt','wb')
        contactStFile.write(store_data)
        contactStFile.close()
        self.serverSocket.close()
        self.addPalSocket.close()
        for i in self.gchatterlist:
            i['chatter'].sendQuit()

        for i in self.chatterlist:
            i.close()
            record = None
            if os.path.exists(i.path+'record.txt') and os.path.getsize(i.path+'record.txt') > 0:
                file = open(i.path+'record.txt','rb')
                filecontent = file.read()
                file.close()
                record = pickle.loads(filecontent)
                if record is not None:
                    record.extend(i.record)
            if record is None:
                record = i.record
            file = codecs.open(i.path+'record.txt','wb')
            file.write(pickle.dumps(record))
            file.close()
        self.logout_signal.emit()
        self.isExisted = False

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

    def consult_all(self):
        consult = socket(AF_INET, SOCK_STREAM)
        consult.settimeout(5)
        try:
            consult.connect(ADDR)
        except:
            print('Connect Server Exception!')
            consult.close()
            return

        for i in self.contactlist:
            consult.send(('q' + i['contact_id']).encode())
            data = consult.recv(BUFSIZ).decode('utf-8')
            if data == 'n' and i['online'] == True:
                self.grouplist[i['group_index']]['pal_online']-=1
                i['contact_ip'] = 'n'
                i['online'] = False
            if data != 'n' and i['online'] == False:
                self.grouplist[i['group_index']]['pal_online']+=1
                i['contact_ip'] = data
                i['online'] = True
        consult.close()
        self.refresh_signal.emit()


    def refresh(self):
        for i in range(len(self.grouplist)):
            groupdic = self.grouplist[i]
            groupname = groupdic['group_name'] + ' ' + str(
                groupdic['pal_online']) + '/' + str(groupdic['pal_count'])
            groupdic['group'].setText(0, groupname)
        for i in self.contactlist:
            text = i['contact'].text(0).split('\n ')
            if len(text)>1:
                i['contact'].setText(0, 'id:' + i['contact_id'] + ' ip:' + i['contact_ip']+'\n '+text[1])
            else:
                i['contact'].setText(0, 'id:' + i['contact_id'] + ' ip:' + i['contact_ip'])

    def search(self, key):
        for i, k in enumerate(self.grouplist):
            if key == k['group_name']:
                return i
        if key == self.username:
            return -1
        for i, k in enumerate(self.contactlist):
            if key == k['contact_id']:
                return i
        return -2

    def search_item(self, key):
        for i, k in enumerate(self.contactlist):
            if key == k['contact']:
                return i, 0
        for i, k in enumerate(self.gchatterlist):
            if key == k['treeItem']:
                return i, 1
        return -1, -1

    def search_ip(self, key):
        # private ip
        for i, k in enumerate(self.contactlist):
            if key == k['contact_ip']:
                return i, 0
        # multicast address
        for i, k in enumerate(self.gchatterlist):
            if key == k['port']:
                return i, 1
        return -1, -1

    def chatbox(self):
        selectItem = self.ui.treeWidget.currentItem()
        index, flag = self.search_item(selectItem)
        if flag == 0:
            text = selectItem.text(0).split('\n ')[0]
            selectItem.setText(0,text)
            self.chatterlist[index].show()
        elif flag == 1:
            self.gchatterlist[index]['chatter'].show()

    def contextMenuEvent(self,a):
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
        num,flag = self.search_item(selectItem)
        for i in self.contactlist:
            if i['contact'] is selectItem:
                self.grouplist[i['group_index']]['pal_count'] -= 1
                if i['online'] is True:
                    self.grouplist[i['group_index']]['pal_online'] -= 1
                index = selectItem.parent().indexOfChild(selectItem)
                selectItem.parent().takeChild(index)
                self.contactlist.remove(i)

        if flag == 0:
            self.chatterlist.remove(self.chatterlist[num])
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
        if flag == 1:
            # add group chatting
            text, ok = QInputDialog.getText(self, 'Input',
                                            'GroupChatter Name:')
            if ok:
                if self.search(text) >= 0:
                    QMessageBox.information(self, "Warning", 'Name Existed')
                else:
                    self.createGchatter(text)

    def createGchatter(self, text):
        # generate the non-used address
        while (True):
            port = multicastAddress.generatePort()
            if self.search_ip(port)[0] == -1:
                break
        treeItem = QTreeWidgetItem(self.ui.treeWidget)
        treeItem.setText(0, '(group chatter)' + text)

        Gchatter = groupchatter.GroupChatter(self.username, self.ip, text,
                                             port)
        Gchatter.consult_signal.connect(self.replyPallist)
        Gchatter.addmem_signal.connect(self.sendMulticast)
        Gchatter.show()

        Gchatterdic = {
            'name': text,
            'chatter': Gchatter,
            'port': port,
            'treeItem': treeItem
        }
        self.gchatterlist.append(Gchatterdic)

    def joinGchatter(self, multicast_info):
        treeItem = QTreeWidgetItem(self.ui.treeWidget)
        treeItem.setText(0, '(group chatter)' + multicast_info['name'])

        Gchatter = groupchatter.GroupChatter(self.username, self.ip,
                                             multicast_info['name'],
                                             multicast_info['port'])
        Gchatter.consult_signal.connect(self.replyPallist)
        Gchatter.addmem_signal.connect(self.sendMulticast)
        Gchatter.join(multicast_info['mem_info'])
        Gchatter.show()

        Gchatterdic = {
            'name': multicast_info['name'],
            'chatter': Gchatter,
            'port': multicast_info['port'],
            'treeItem': treeItem
        }
        self.gchatterlist.append(Gchatterdic)

    def replyPallist(self, port):
        index, flag = self.search_ip(port)
        if flag == 1:
            self.gchatterlist[index]['chatter'].addMember(self.contactlist)

    def sendMulticast(self, multicast_info):
        index, flag = self.search_ip(multicast_info['target'])
        if flag == 0:
            self.chatterlist[index].sendMulticast(multicast_info)

    def closeEvent(self,event):
        reply = QMessageBox.question(self, 'Warning',"Do you want to quit?",QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.logout()
            event.accept()
        else:
            event.ignore()
