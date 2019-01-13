# -*- coding: utf-8 -*-

import os
import time
import random
import pickle
import struct
import codecs
import threading
from socket import *

import PyQt5.QtCore as PQC
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QWidget, QCheckBox, QAction, QDialog

from Ui_groupchatter import Ui_Form
from static_var import *
import addmem


class GroupChatter(QWidget):
    write_signal = PQC.pyqtSignal(dict)
    consult_signal = PQC.pyqtSignal(int)
    addmem_signal = PQC.pyqtSignal(dict)

    def __init__(self, *args):
        super(GroupChatter, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.id = args[0]
        self.ip = args[1]
        self.name = args[2]
        self.port = args[3]
        self.record = ''
        self.rowCount = 1
        self.memberlist = [{'id': self.id, 'ip': self.ip}]
        self.setWindowTitle(self.name)

        self.ui.tableWidget.setRowCount(self.rowCount)
        self.ui.tableWidget.setItem(0, 0, QTableWidgetItem(self.id))
        self.ui.tableWidget.setItem(0, 1, QTableWidgetItem(self.ip))
        self.ui.tableWidget.setColumnWidth(0,135)
        self.ui.tableWidget.setColumnWidth(1,135)
        self.candidate = None

        self.connect = None

        self.multicastSocket = socket(AF_INET, SOCK_STREAM)
        self.multicastSocket.bind((self.ip, self.port))
        self.multicastSocket.listen(10)
        self.threadsocket = threading.Thread(
            target=self.recvMessage, name='multicast')
        self.threadsocket.start()

        self.ui.send_btn.clicked.connect(self.sendMessage)
        self.write_signal.connect(self.container)
        self.ui.addMem_btn.clicked.connect(
            lambda: self.consult_signal.emit(self.port))

    def sendData(self, itype, content):
        data = {
            'Type': itype,
            'id': self.id,
            'ip': self.ip,
            'data': content
        }
        data = pickle.dumps(data)
        for i in self.memberlist:
            self.connect = socket(AF_INET, SOCK_STREAM)
            self.connect.settimeout(1)
            try:
                self.connect.connect((i['ip'], self.port))
                self.connect.send(data)
                self.connect.close()
            except:
                continue
        self.connect = None

    def sendMessage(self):
        text = self.ui.send_textEdit.toPlainText()
        if text:
            self.sendData('message', text)
            self.ui.send_textEdit.clear()

    def sendNewMem(self, id, ip):
        self.sendData('newmem', {'id': id, 'ip': ip})

    def sendQuit(self):
        self.sendData('quit','')

    def recvMessage(self):
        while (True):
            try:
                clientSocket, clientInfo = self.multicastSocket.accept()
                recvData = clientSocket.recv(BUFSIZ)
                if recvData:
                    self.write_signal.emit(pickle.loads(recvData))
            except Exception:
                break


    def container(self, data):
        # data = pickle.loads(rawData)
        if data['Type'] == 'message':
            display = '\n' + data['id'] + ' (' + data['ip'] + ')' + '\n' + data['data']
            self.record += display
            self.ui.info_textEdit.setText(self.record)
        if data['Type'] == 'newmem' and data['ip']!= self.ip:
            self.rowCount += 1
            self.memberlist.append(data['data'])
            self.ui.tableWidget.setRowCount(self.rowCount)
            self.ui.tableWidget.setItem(self.rowCount - 1, 0,
                                        QTableWidgetItem(data['data']['id']))
            self.ui.tableWidget.setItem(self.rowCount - 1, 1,
                                        QTableWidgetItem(data['data']['ip']))
        if data['Type'] == 'quit':
            if data['ip'] == self.ip:
                self.multicastSocket.close()
            else:
                for i in range(self.rowCount):
                    if self.ui.tableWidget.item(i,0):
                        if self.ui.tableWidget.item(i,0).text() == data['id']:
                            self.ui.tableWidget.removeRow(i)
                            self.rowCount -= 1
                            self.ui.tableWidget.setRowCount(self.rowCount)
                            self.memberlist.remove(self.memberlist[i])

    def addMember(self, pal_list):
        self.candidate = addmem.AddMem()
        table = self.candidate.ui.tableWidget
        table.setRowCount(len(pal_list))
        for i, j in enumerate(pal_list):
            isEmpty = self.ui.tableWidget.findItems(j['contact_ip'],
                                                    PQC.Qt.MatchExactly)
            check = QTableWidgetItem()
            check.setCheckState(PQC.Qt.Unchecked)
            check.setText(j['contact_id'])
            table.setItem(i, 0, check)
            table.setItem(i, 1, QTableWidgetItem(j['contact_ip']))
            if isEmpty or j['online'] == False:
                check.setFlags(PQC.Qt.NoItemFlags)
                table.item(i, 1).setFlags(PQC.Qt.NoItemFlags)
        if self.candidate.exec() == QDialog.Accepted:
            for i, j in enumerate(pal_list):
                if table.item(i, 0).checkState() == PQC.Qt.Checked and table.item(i, 0).flags() != PQC.Qt.NoItemFlags:
                    self.rowCount += 1
                    self.ui.tableWidget.setRowCount(self.rowCount)
                    self.ui.tableWidget.setItem(
                        self.rowCount - 1, 0,
                        QTableWidgetItem(j['contact_id']))
                    self.ui.tableWidget.setItem(
                        self.rowCount - 1, 1,
                        QTableWidgetItem(j['contact_ip']))
                    self.sendNewMem(j['contact_id'], j['contact_ip'])
                    multicast_info = {
                        'target': j['contact_ip'],
                        'mem_info': self.memberlist,
                        'port': self.port,
                        'name': self.name
                    }
                    self.addmem_signal.emit(multicast_info)
                    self.memberlist.append({'id':j['contact_id'],'ip':j['contact_ip']})
                    time.sleep(0.1)

    def join(self,mem_info):
        self.rowCount += len(mem_info)
        self.ui.tableWidget.setRowCount(self.rowCount)
        for i,j in enumerate(mem_info):
            self.memberlist.append({'id':j['id'],'ip':j['ip']})
            self.ui.tableWidget.setItem(i+1,0,QTableWidgetItem(j['id']))
            self.ui.tableWidget.setItem(i+1,1,QTableWidgetItem(j['ip']))
