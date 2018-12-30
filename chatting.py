# -*- coding: utf-8 -*-

import random
import re
from socket import *

import PyQt5.QtCore as PQC
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem, QWidget, QMenu, QAction

from Ui_chatting import Ui_Form
from static_var import *


class Chatting(QWidget):
    write_signal = PQC.pyqtSignal(str)
    def __init__(self, *args):
        super(Chatting, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.username = args[0]
        self.ip = args[1]
        self.target = args[2]
        self.target_info = self.target['contact_id']+' ('+self.target['contact_ip']+')'
        self.record=''

        self.connect = None

        self.ui.send_pushButton.clicked.connect(self.sendMessage)
        self.write_signal.connect(self.writeText)

    def sendMessage(self):
        data = self.ui.send_textEdit.toPlainText()
        if data:
            self.connect =socket(AF_INET, SOCK_STREAM)
            self.connect.connect((self.target['contact_ip'],CHAT_PORT))
            self.connect.send(data.encode())
            self.ui.send_textEdit.clear()
            self.connect.close()

    def recvMessage(self,recvSocket):
        recvData = recvSocket.recv(BUFSIZ)
        if recvData:
            self.write_signal.emit(recvData.decode('utf-8'))
        recvSocket.close()

    def writeText(self,text):
        self.record += '\n'+self.target_info+'\n'+text
        self.ui.info_display.setText(self.record)
