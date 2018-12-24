# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication

import welcome

if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome = welcome.Welcome()
    welcome.show()
    app.exec_()
