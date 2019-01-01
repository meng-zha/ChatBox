# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from socket import *
import threading

from Ui_sendfile import Ui_SendFile
from static_var import *


class SendFile(QDialog):
    def __init__(self, *args):
        super(SendFile, self).__init__(*args)
        self.ui = Ui_SendFile()
        self.ui.setupUi(self)
