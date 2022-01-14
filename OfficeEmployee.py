from PyQt5.QtCore import QObject, pyqtSlot, QDate
from PyQt5.QtWidgets import *

class Register(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Office Worker Register Screen")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
