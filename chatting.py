# -*- coding: utf-8 -*-

import random
import re
from socket import *

import PyQt5.QtCore as PQC
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem, QWidget

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
        self.ui.info_display.setText(self.target)

        self.connect = socket(AF_INET,SOCK_STREAM)
        # self.connect.connect((self.target[17:],CHAT_PORT))

        self.ui.send_pushButton.clicked.connect(self.sendMessage)

    def sendMessage(self):
        data = self.ui.send_textEdit.document()
        if data is not None:
            self.connect.send(data.encode())