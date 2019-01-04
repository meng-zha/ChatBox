# -*- coding: utf-8 -*-

import os
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
    consult_signal = PQC.pyqtSignal(str)
    addmem_signal = PQC.pyqtSignal(dict)

    def __init__(self, *args):
        super(GroupChatter, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.id = args[0]
        self.ip = args[1]
        self.name = args[2]
        self.address = args[3]
        self.record = ''
        self.rowCount = 1
        self.memberlist = [{'id': self.id, 'ip': self.ip}]

        self.ui.tableWidget.setRowCount(self.rowCount)
        self.ui.tableWidget.setItem(0, 0, QTableWidgetItem(self.id))
        self.ui.tableWidget.setItem(0, 1, QTableWidgetItem(self.ip))
        self.candidate = None

        self.connect = None

        self.multicastSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        try:
            self.multicastSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        except AttributeError:
            pass
        self.multicastSocket.bind(('', MULTICAST_PORT))
        addr = inet_pton(AF_INET, self.address)
        interface = inet_pton(AF_INET, self.ip)
        self.multicastSocket.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP,
                                        addr + interface)
        self.threadMCsocket = threading.Thread(
            target=self.recvMessage, name='multicast')
        self.threadMCsocket.start()

        self.ui.send_btn.clicked.connect(self.sendMessage)
        self.write_signal.connect(self.container)
        self.ui.addMem_btn.clicked.connect(
            lambda: self.consult_signal.emit(self.address))

    def sendData(self, itype, content):
        if itype != 'file':
            data = {
                'Type': itype,
                'id': self.id,
                'ip': self.ip,
                'data': content
            }
            data = pickle.dumps(data)
            self.connect = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
            self.connect.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, 20)

            self.connect.sendto(data, (self.address, MULTICAST_PORT))
            self.connect.close()
            self.connect = None
        else:
            if self.connect is None:
                self.connect = socket(AF_INET, SOCK_STREAM)
                self.connect.connect((self.target['contact_ip'], CHAT_PORT))
            if content == '':
                self.connect.close()
                self.connect = None
            else:
                self.connect.send(content)

    def sendMessage(self):
        text = self.ui.send_textEdit.toPlainText()
        if text:
            self.sendData('message', text)
            self.ui.send_textEdit.clear()

    def sendNewMem(self, id, ip):
        self.sendData('newmem', {'id': id, 'ip': ip})

    def recvMessage(self):
        while (True):
            recvData = self.multicastSocket.recv(BUFSIZ)
            if recvData:
                try:
                    self.write_signal.emit(pickle.loads(recvData))
                except:
                    self.write_signal.emit({'Type': 'file', 'data': recvData})
            else:
                break

    def container(self, data):
        # data = pickle.loads(rawData)
        if data['Type'] == 'message':
            self.record += '\n' + data['ip'] + data['id'] + '\n' + data['data']
            self.ui.info_textEdit.setText(self.record)
        if data['Type'] == 'addmem':
            self.rowCount += 1
            self.ui.tableWidget.setRowCount(self.rowCount)
            self.ui.tableWidget.setItem(self.rowCount - 1, 0,
                                        QTableWidgetItem(j['contact_id']))
            self.ui.tableWidget.setItem(self.rowCount - 1, 1,
                                        QTableWidgetItem(j['contact_ip']))

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
                self.ui.tableWidget.item(i, 1).setFlags(PQC.Qt.NoItemFlags)
        if self.candidate.exec() == QDialog.Accepted:
            for i, j in enumerate(pal_list):
                if table.item(i, 0).checkState() == PQC.Qt.Checked:
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
                        'addr': self.address,
                        'name': self.name
                    }
                    self.addmem_signal.emit(multicast_info)

    def join(self,mem_info):
        self.rowCount += len(mem_info)
        self.ui.tableWidget.setRowCount(self.rowCount)
        for i,j in enumerate(mem_info):
            self.ui.tableWidget.setItem(i+1,0,QTableWidgetItem(j['id']))
            self.ui.tableWidget.setItem(i+1,1,QTableWidgetItem(j['ip']))
