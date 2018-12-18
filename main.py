# -*- coding: utf-8 -*-

import welcome
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome = welcome.Welcome()
    welcome.show()
    sys.exit(app.exec_())
