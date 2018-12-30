# -*- coding: utf-8 -*-

import random
import re
from socket import *

import PyQt5.QtCore as PQC
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem, QWidget, QMenu, QAction

from Ui_chatting import Ui_Form
from static_var import *


class Chatting(QWidget):
    def __init__(self, *args):
        super(Chatting, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.username = args[0]
        self.ip = args[1]
        self.target = args[2]
        self.ui.info_display.setText(self.target['contact_id']+' '+self.target['contact_ip'])

        self.connect = None

        self.ui.send_pushButton.clicked.connect(self.sendMessage)

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
        if not recvData:
            self.ui.info_display.setText(recvData.decoding('utf-8'))
        recvSocket.close()
