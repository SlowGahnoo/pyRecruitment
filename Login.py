from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from util import *

from DBManager import DBManagement

import Candidate, Employer, OfficeEmployee

dbman = DBManagement("test.db")

type_dict = {
        "Candidate": Candidate,
        "Employer":  Employer,
        "Office Employee": OfficeEmployee
        }

class Login(QWidget):
    def __init__(self, mainwindow):
        super().__init__()
        self.mainwindow = mainwindow
        self.usrname = QLineEdit()
        self.passwd = QLineEdit()
        self.passwd.setEchoMode(QLineEdit.Password)

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

    def login_user(self):
        username = self.usrname.text()
        password = self.passwd.text()
        _id = dbman.loginUser(username, password)
        if _id:
            return _id
        else:
            print("User doesn't exist")


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = Login(self)
        self.w.show()
        self.w.login_button.clicked.connect(self.switch_main)
        self.w.register.clicked.connect(self.switch_register)
        self.setCentralWidget(self.w)
        self.resize(640, 480)

    def switch_register(self):
        self.type = self.w.getType()
        self.w = type_dict[self.type].Register(self)
        self.setCentralWidget(self.w)

    def switch_from_register(self):
        _id = self.w.getID()
        if _id:
            self.w = type_dict[self.type].Widget(_id)
            self.setCentralWidget(self.w)

    def switch_main(self):
        _id = self.w.login_user()
        self.type = self.w.getType()
        if _id:
            self.w = type_dict[self.type].Widget(_id)
            self.setCentralWidget(self.w)

def main():
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
