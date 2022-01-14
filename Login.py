from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
import Candidate, Employer, OfficeEmployee
from pyRecruitment import *

type_dict = {
        "Candidate": Candidate,
        "Employer":  Employer,
        "Office Employee": OfficeEmployee
        }

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.usrname = QLineEdit()
        self.passwd = QLineEdit()

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("<b>Login Screen</b>", alignment=QtCore.Qt.AlignCenter))

        typelayout = QHBoxLayout()
        self.type = QComboBox()
        self.type.addItems(type_dict.keys())
        typelabel = QLabel("I am a: ")
        typelabel.setFixedSize(typelabel.sizeHint())
        typelayout.addWidget(typelabel)
        typelayout.addWidget(self.type)

        usrlayout = QHBoxLayout()
        usrlayout.addWidget(QLabel("Username:"))
        usrlayout.addWidget(self.usrname)

        passlayout = QHBoxLayout()
        passlayout.addWidget(QLabel("Password:"))
        passlayout.addWidget(self.passwd)

        self.layout.addLayout(typelayout)
        self.layout.addLayout(usrlayout)
        self.layout.addLayout(passlayout)

        self.login_button = QPushButton("Login")
        self.layout.addWidget(self.login_button)

        self.layout.addStretch()
        self.layout.addWidget(QLabel("Don't have an account?"))
        self.register = QPushButton("Register")
        self.layout.addWidget(self.register)

        self.setLayout(self.layout)

    def getType(self):
        return str(self.type.currentText())

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = Login()
        self.w.show()
        self.w.login_button.clicked.connect(self.switch_main)
        self.w.register.clicked.connect(self.switch_register)
        self.setCentralWidget(self.w)
        self.resize(640, 480)

    def switch_register(self):
        self.w = type_dict[self.w.getType()].Register()
        self.setCentralWidget(self.w)

    def switch_main(self):
        self.w = Widget()
        self.setCentralWidget(self.w)

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
        
