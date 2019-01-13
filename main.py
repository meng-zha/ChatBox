# -*- coding: utf-8 -*-

import sys
import qdarkstyle
from PyQt5.QtWidgets import QApplication

import welcome

if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome = welcome.Welcome()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    welcome.show()
    app.exec_()
