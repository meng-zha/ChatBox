# -*- coding: utf-8 -*-

import os
import random
import re
import json
import pickle
import codecs
import threading
from socket import *

import PyQt5.QtCore as PQC
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem, QWidget, QMenu, QAction, QFileDialog, QDialog

from Ui_chatting import Ui_Form
from static_var import *
import sendfile


class Chatting(QWidget):
    write_signal = PQC.pyqtSignal(dict)

    def __init__(self, *args):
        super(Chatting, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.username = args[0]
        self.ip = args[1]
        self.target = args[2]
        self.fileName = ''
        self.saveName = ''
        self.target_info = self.target['contact_id'] + ' (' + self.target[
            'contact_ip'] + ')'
        self.record = ''
        self.sendDialog = None

        self.connect = None

        self.ui.send_pushButton.clicked.connect(self.sendMessage)
        self.ui.files_pushButton.clicked.connect(self.sendFile)
        self.write_signal.connect(self.container)

    def sendData(self, itype, content):
        self.connect = socket(AF_INET, SOCK_STREAM)
        self.connect.connect((self.target['contact_ip'], CHAT_PORT))
        data = {
            'Type': itype,
            'id': self.target['contact_id'],
            'ip': self.target['contact_ip'],
            'data': content
        }
        data = pickle.dumps(data)
        # self.connect.send(data.encode())
        self.connect.send(data)
        self.connect.close()

    def sendMessage(self):
        text = self.ui.send_textEdit.toPlainText()
        if text:
            self.sendData('message', text)
            self.ui.send_textEdit.clear()

    def sendFile(self):
        self.fileName = QFileDialog.getOpenFileName(self, 'Send File', './')[0]
        if self.fileName:
            self.sendDialog = sendfile.SendFile()
            self.sendDialog.ui.filename_label.setText(
                self.fileName.split("/")[-1])
            self.sendDialog.ui.ok_pushButton.clicked.connect(self.queryFile)
            self.sendDialog.ui.reject_pushButton.clicked.connect(
                self.cancelFile)
            self.sendDialog.show()

    def cancelFile(self):
        self.sendDialog.close()
        del self.sendDialog

    def queryFile(self):
        self.sendDialog.ui.ok_pushButton.setDisabled(True)
        self.sendData('query', self.fileName)

    def recvMessage(self, recvSocket):
        recvData = recvSocket.recv(BUFSIZ)
        if recvData:
            # self.write_signal.emit(recvData.decode('utf-8'))
            self.write_signal.emit(pickle.loads(recvData))
        recvSocket.close()

    def container(self, data):
        # data = pickle.loads(rawData)
        if data['Type'] == 'message':
            self.record += '\n' + self.target_info + '\n' + data['data']
            self.ui.info_display.setText(self.record)
        if data['Type'] == 'query':
            info = 'File {} from ip={} id={}'.format(data['data'], data['ip'],
                                                    data['id'])
            isrecv = QMessageBox.information(self, "query for receive", info,
                                            QMessageBox.Yes, QMessageBox.No)
            if isrecv == QMessageBox.Yes:
                self.saveName = QFileDialog.getSaveFileName(
                    self, "save file", data['data'])[0]
                if self.saveName:
                    if os.path.exists(self.saveName):
                        os.remove(self.saveName)
                    self.sendData('reply', 'ACK')
            else:
                self.sendData('reply', 'NAK')
        if data['Type'] == 'reply' and self.sendDialog is not None:
            if data['data'] == 'NAK':
                self.cancelFile()
                QMessageBox.information(self, "Warning",
                                        'Sending File is rejected!')
            else:
                size = os.path.getsize(self.fileName)
                iter = 0
                file = open(self.fileName, 'rb')
                while(True):
                    filedata = file.read(BUFSIZ-240)
                    if not filedata:
                        break
                    self.sendData('file', filedata)
                    iter += 1
                    self.sendDialog.ui.progressBar.setValue(iter*BUFSIZ/size)
                file.close()
                self.sendData('file','')
                self.sendDialog.close()
                del self.sendDialog
        if data['Type'] == 'file':
            if(data['data']==''):
                QMessageBox.information(self, '','Successful!')
            else:
                file = open(self.saveName, 'ab')
                file.write(data['data'])
                file.close()