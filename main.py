import welcome
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = welcome.Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
