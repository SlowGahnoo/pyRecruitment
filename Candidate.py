from PyQt5.QtCore import QObject, pyqtSlot, QDate, QDate, QDateTime
from PyQt5.QtWidgets import *

from DBManager import *

dbman = DBManagement("test.db")

class Register(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Username"))
        self.usrname = QLineEdit()
        self.layout.addWidget(self.usrname)
        self.layout.addWidget(QLabel("Password"))
        self.passwd = QLineEdit()
        self.passwd.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.passwd)
        self.layout.addWidget(QLabel("Confirm Password"))
        self.cpasswd = QLineEdit()
        self.cpasswd.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.cpasswd)
        self.layout.addWidget(QLabel("Email"))
        self.email = QLineEdit()
        self.layout.addWidget(self.email)

        middle = QHBoxLayout()

        left = QVBoxLayout()
        left.addWidget(QLabel("Name"))
        self.name = QLineEdit()
        left.addWidget(self.name)


        right = QVBoxLayout()
        right.addWidget(QLabel("Surname"))
        self.surname = QLineEdit()
        right.addWidget(self.surname)

        middle.addLayout(left)
        middle.addLayout(right)
        self.layout.addLayout(middle)

        self.layout.addWidget(QLabel("Sex"))
        self.sex = QComboBox()
        self.sex.addItems(["M", "F"])
        self.layout.addWidget(self.sex)

        uni = dbman.getUniversities()
        self.layout.addWidget(QLabel("University"))
        self.uni = QComboBox()
        self.uni.addItems(uni)
        self.layout.addWidget(self.uni)

        dpt = dbman.getDepartment(uni[0])
        self.layout.addWidget(QLabel("Department"))
        self.dpt = QComboBox()
        self.dpt.addItems(dpt)
        self.layout.addWidget(self.dpt)

        self.layout.addWidget(QLabel("Phone number"))
        self.phone = QLineEdit()
        self.layout.addWidget(self.phone)

        middle = QHBoxLayout()

        left = QVBoxLayout()
        left.addWidget(QLabel("Street"))
        self.street = QLineEdit()
        left.addWidget(self.street)


        right = QVBoxLayout()
        right.addWidget(QLabel("Street number"))
        self.street_num = QLineEdit()
        self.street_num.setFixedSize(self.street_num.sizeHint())
        right.addWidget(self.street_num)

        middle.addLayout(left)
        middle.addLayout(right)
        self.layout.addLayout(middle)

        self.layout.addWidget(QLabel("Zip code"))
        self.zipcode = QLineEdit()
        self.layout.addWidget(self.zipcode)

        self.bday = QDateEdit()
        self.bday.setDisplayFormat("yyyy/MM/dd")
        self.layout.addWidget(self.bday)

        self.layout.addStretch()

        self.register = QPushButton("Register")
        self.register.setEnabled(False)
        self.layout.addWidget(self.register)


        self.fields = [
                self.usrname,
                self.passwd,
                self.cpasswd,
                self.name,
                self.surname,
                self.email,
                self.street,
                self.street_num,
                self.zipcode
        ]
        for field in self.fields:
            field.textChanged[str].connect(self.check_disable)

        self.uni.currentIndexChanged[str].connect(self.change_dpt)
        self.register.clicked.connect(self.register_user)
        # field.textChanged[str].connect(self.check_disable)

        self.warning = QLabel("")
        self.warning.setStyleSheet("color: red;")
        self.layout.addWidget(self.warning)

        self.setLayout(self.layout)

    @pyqtSlot()
    def change_dpt(self):
        uni = self.uni.currentText()
        dpt = dbman.getDepartment(uni)
        self.dpt.clear()
        self.dpt.addItems(dpt)

    @pyqtSlot()
    def check_disable(self):
        if 0 in [len(s.text()) for s in self.fields]:
            self.register.setEnabled(False)


        elif self.passwd.text() != self.cpasswd.text():
            self.register.setEnabled(False)
            self.warning.setText("Passwords do not match!")

        elif not self.street_num.text().isnumeric():
            self.register.setEnabled(False)
            self.warning.setText("Street number is not numeric")

        elif not self.phone.text().isnumeric() or len(self.phone.text()) > 10:
            self.register.setEnabled(False)
            self.warning.setText("Invalid phone number")

        else:
            self.register.setEnabled(True)
            self.warning.setText("")

    def register_user(self):
        import random

        usr_id = int("".join([str(ord(x)) for x in self.email.text()]))

        login = Login(
                    _id = usr_id,
                    usrname = self.name.text(), 
                    passwd = self.passwd.text(), 
                    email = self.email.text())

        candidate = Candidate(
                _id         = usr_id,
                name        = self.name.text(), 
                surname     = self.surname.text(), 
                sex         = self.sex.currentText(), 
                birthday    = self.bday.date().toString("yyyy-MM-dd"), 
                phone_num   = self.phone.text(), 
                street      = self.street.text(), 
                street_num  = self.street_num.text(),
                zipcode     = self.zipcode.text(),
                email       = self.email.text())

        dbman.pushCandidate(candidate)
        dbman.pushLogin(login)
        dbman.commit()
        print(login)
        print(candidate)

