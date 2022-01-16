from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject, pyqtSlot, QDate

from Cards import *
import Employer
from util import *





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_app)
        self.file_menu.addAction(exit_action)

        self.setCentralWidget(Widget())

    @pyqtSlot()
    def exit_app(self, checked = None):
        print("Exited")
        QApplication.quit()


# d = DBManagement("test.db")
def main():
    app = QApplication([])
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    return app.exec()
