# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from socket import *
import threading

from Ui_addmem import Ui_Dialog
from static_var import *


class AddMem(QDialog):
    def __init__(self, *args):
        super(AddMem, self).__init__(*args)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
