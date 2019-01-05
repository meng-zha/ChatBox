# -*- coding: utf-8 -*-

import os
import threading
import time
import pickle
import codecs
from socket import *

import PyQt5.QtCore as PQC
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem, QWidget, QLabel, QAction, QFileDialog, QDialog, QTableWidgetItem

from Ui_chatting import Ui_Form
from static_var import *
import sendfile


class Chatting(QWidget):
    write_signal = PQC.pyqtSignal(dict)
    createMulticast_signal = PQC.pyqtSignal(dict)
    newsform_signal = PQC.pyqtSignal(str)

    def __init__(self, *args):
        super(Chatting, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.path='./{}/{}/'.format(args[0],args[2]['contact_id'])
        if os.path.exists(self.path)==False:
            os.makedirs(self.path)
        self.username = args[0]
        self.ip = args[1]
        self.target = args[2]
        self.fileName = ''
        self.saveName = ''
        self.target_info = self.target['contact_id'] + ' (' + self.target[
            'contact_ip'] + ')'
        self.record = []
        self.sendDialog = None
        self.emojilist = []
        self.ui.emoji_table.setColumnCount(2)
        self.ui.emoji_table.setRowCount(4)
        self.emojiInit()

        self.connect = None

        self.ui.send_pushButton.clicked.connect(self.sendMessage)
        self.ui.files_pushButton.clicked.connect(self.sendFile)
        self.write_signal.connect(self.container)
        self.ui.emoji_table.cellDoubleClicked.connect(self.sendEmoji)
        self.ui.record_btn.clicked.connect(self.historyRecord)

    def emojiInit(self):
        self.ui.emoji_table.horizontalHeader().setVisible(False)
        self.ui.emoji_table.verticalHeader().setVisible(False)
        self.ui.emoji_table.setColumnWidth(0, 200)
        self.ui.emoji_table.setColumnWidth(1, 200)
        for i in range(4):
            self.ui.emoji_table.setRowHeight(i, 200)
            icon = QLabel('')
            icon.setPixmap(
                QtGui.QPixmap("./emoji/{}.gif".format(2 * i + 1)).scaled(
                    195, 195))
            self.ui.emoji_table.setCellWidget(i, 0, icon)
            icon2 = QLabel('')
            icon2.setPixmap(
                QtGui.QPixmap("./emoji/{}.gif".format(2 * i + 2)).scaled(
                    195, 195))
            self.ui.emoji_table.setCellWidget(i, 1, icon2)

    def sendData(self, itype, content):
        selfconnect = socket(AF_INET, SOCK_STREAM)
        selfconnect.connect((self.ip,CHAT_PORT))
        if itype != 'file' and itype!= 'emoji':
            data = {
                'Type': itype,
                'id': self.target['contact_id'],
                'ip': self.target['contact_ip'],
                'data': content
            }
            data = pickle.dumps(data)
            self.connect = socket(AF_INET, SOCK_STREAM)
            self.connect.settimeout(5)
            try:
                self.connect.connect((self.target['contact_ip'], CHAT_PORT))
                self.connect.send(data)
                selfconnect.send(data)
            except:
                print('Error')
            self.connect.close()
            self.connect = None

        if itype == 'emoji':
            data = b'EMOJI'+content
            self.connect = socket(AF_INET, SOCK_STREAM)
            self.connect.settimeout(5)
            try:
                self.connect.connect((self.target['contact_ip'], CHAT_PORT))
                time.sleep(0.1)
                self.connect.send(data)
                selfconnect.send(data)
            except:
                print('Error')
            self.connect.close()
            self.connect = None

        if itype == 'file':
            if self.connect is None:
                self.connect = socket(AF_INET, SOCK_STREAM)
                self.connect.connect((self.target['contact_ip'], CHAT_PORT))
            if content == '':
                self.connect.close()
                self.connect = None
                self.connect = socket(AF_INET, SOCK_STREAM)
                self.connect.connect((self.target['contact_ip'], CHAT_PORT))
                self.connect.send(b'END')
                self.connect.close()
                self.connect = None
            else:
                self.connect.send(content)

    def sendEmoji(self, i, j):
        file = open("./emoji/{}.gif".format(2 * i + j +  1 ), 'rb')
        filedata = file.read()
        file.close()
        self.sendData('emoji', filedata)

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

    def sendMulticast(self, multicast_info):
        self.sendData('multicast', multicast_info)

    def insertEmoji(self, filename, url):
        self.ui.info_display.insertHtml("<img src='" + url + "'/>")

        movie = QtGui.QMovie(filename)
        movie.setCacheMode(QtGui.QMovie.CacheNone)
        movie.frameChanged.connect(self.refreshMovie)
        self.emojilist[-1]['movie']=movie
        movie.start()

    def searchEmoji(self,item):
        for i in self.emojilist:
            if i['movie'] == item:
                return i['url']

    def refreshMovie(self, num):
        movie = self.sender()
        self.ui.info_display.document().addResource(
            QtGui.QTextDocument.ImageResource, PQC.QUrl(self.searchEmoji(movie)),
            movie.currentPixmap())
        self.ui.info_display.setLineWrapColumnOrWidth(
            self.ui.info_display.lineWrapColumnOrWidth())

    def cancelFile(self):
        self.sendDialog.close()
        del self.sendDialog

    def queryFile(self):
        self.sendDialog.ui.ok_pushButton.setDisabled(True)
        self.sendData('query', self.fileName)

    def recvMessage(self, recvSocket):
        while (True):
            recvData = recvSocket.recv(BUFSIZ)
            if recvData:
                try:
                    self.write_signal.emit(pickle.loads(recvData))
                except:
                    if recvData[0:5] == b'EMOJI':
                        self.write_signal.emit({'Type': 'emoji', 'data': recvData[5:]})
                    else:
                        self.write_signal.emit({'Type': 'file', 'data': recvData})
            else:
                break
        recvSocket.close()

    def container(self, data):
        # data = pickle.loads(rawData)
        if data['Type'] == 'message':
            display = '\n' + self.target_info + '\n' + data['data']
            self.ui.info_display.insertPlainText(display)
            self.newsform_signal.emit(self.username)
            self.record.append(data)

        if data['Type'] == 'emoji':
            self.record.append(data)
            display = '\n' + self.target_info + '\n'
            self.ui.info_display.insertPlainText(display)
            number = len(self.emojilist)
            filePath = '{}emoji{}.gif'.format(self.path,number)
            file = codecs.open(filePath, 'wb')
            self.emojilist.append({'url':'emoji{}'.format(number),'movie':None})
            file.write(data['data'])
            file.close()
            self.insertEmoji(filePath, 'emoji{}'.format(number))

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
                while (True):
                    filedata = file.read(BUFSIZ)
                    if not filedata:
                        break
                    self.sendData('file', filedata)
                    iter += 1
                    self.sendDialog.ui.progressBar.setValue(
                        iter * BUFSIZ / size)
                file.close()
                self.sendData('file', '')
                self.sendDialog.close()
                del self.sendDialog

        if data['Type'] == 'multicast':
            self.createMulticast_signal.emit(data['data'])

        if data['Type'] == 'file':
            if (data['data'] == b'END'):
                QMessageBox.information(self, '', 'Successful!')
            else:
                file = codecs.open(self.saveName, 'ab')
                file.write(data['data'])
                file.close()

    def historyRecord(self):
        if os.path.exists(self.path+'record.txt') and os.path.getsize(self.path+'record.txt') > 0:
            file = open(self.path+'record.txt','rb')
            file_content = file.read()
            file.close()
            record = pickle.loads(file_content)
            if record is not None:
                self.ui.info_display.moveCursor(QtGui.QTextCursor.Start,QtGui.QTextCursor.MoveAnchor)
                self.ui.info_display.clear()
                for i in record:
                    self.container(i)

            self.ui.info_display.moveCursor(QtGui.QTextCursor.End,QtGui.QTextCursor.MoveAnchor)
            os.remove(self.path+'record.txt')
