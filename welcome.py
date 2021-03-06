# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog,QMessageBox
from socket import *
import threading

from Ui_welcome import Ui_Dialog
from static_var import *
import pallist


class Welcome(QDialog):
    def __init__(self, *args):
        super(Welcome, self).__init__(*args)
        # loadUi('welcome.ui', self)
        # TODO:进行画面字体等调整
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.hints.hide()  # hide the hints at first
        self.ui.username_lineEdit.setText('2015011463')
        self.ui.password_lineEdit.setText('net2018')

        self.log_flag = False  # while closed to justify whether to set up list
        self.pal_list = None

        self.ui.login_button.clicked.connect(self.login)

    def login(self):
        # sign in with the username and password
        username = self.ui.username_lineEdit.text()
        password = self.ui.password_lineEdit.text()

        data = username + '_' + password
        recv = ''
        c = socket(AF_INET, SOCK_STREAM)
        c.settimeout(3)
        try:
            c.connect(ADDR)
            c.send(('q'+username).encode())
            recv = c.recv(BUFSIZ).decode('utf-8')
        except:
            QMessageBox.information(self, "Warning", 'Connect Server Exception!')
            return
        if recv != 'n':
            QMessageBox.information(self, "Warning", 'User Has Logged In!\nBut You kicked it!')
        
        try:
            c.send(data.encode())   
            recv = c.recv(BUFSIZ).decode('utf-8')
        except:
            QMessageBox.information(self, "Warning", 'Connect Server Exception!')
            return

        if recv != 'lol':
            self.ui.hints.show()
        else:
            self.ui.hints.hide()
            self.accept(username)

        c.close()

    def accept(self, username):
        self.log_flag = True
        self.hide()
        del self.pal_list  #unbind the port of server socket
        self.pal_list = pallist.PalList(username, get_host_ip())
        self.pal_list.show()

        self.pal_list.logout_signal.connect(self.show)
        self.pal_list.logout_signal.connect(self.pal_list.close)


def get_host_ip():
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip
