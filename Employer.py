from PyQt5.QtCore import QObject, pyqtSlot, QDate
from PyQt5.QtWidgets import *

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

        self.layout.addWidget(QLabel("Company Name"))
        self.company = QLineEdit()
        self.layout.addWidget(self.company)
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
                self.company,
        ]
        for field in self.fields:
            field.textChanged[str].connect(self.check_disable)

        self.warning = QLabel("")
        self.warning.setStyleSheet("color: red;")
        self.layout.addWidget(self.warning)

        self.setLayout(self.layout)

    @pyqtSlot()
    def check_disable(self):
        if 0 in [len(s.text()) for s in self.fields]:
            self.register.setEnabled(False)
        elif self.passwd.text() != self.cpasswd.text():
            self.register.setEnabled(False)
            self.warning.setText("Passwords do not match!")
        else:
            self.register.setEnabled(True)
            self.warning.setText("")


class RightPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.description = QPlainTextEdit()
        self.send = QPushButton("Send")
        self.clear = QPushButton("Clear")
        self.quit = QPushButton("Quit")
        self.plot = QPushButton("Plot")
        self.send.setEnabled(False)

        self.salary = QLineEdit()
        self.location = QLineEdit()

        # Right
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("Location"))
        self.layout.addWidget(self.location)
        self.layout.addWidget(QLabel("Salary"))
        self.layout.addWidget(self.salary)
        self.layout.addWidget(QLabel("Description"))
        self.layout.addWidget(self.description)

        self.telework = QCheckBox()
        self.telework.setText("Telework")
        self.layout.addWidget(self.telework)

        self.layout.addWidget(QLabel("Submission Deadline"))
        self.calendar = QCalendarWidget()
        self.layout.addWidget(self.calendar)


        self.layout.addWidget(self.send)
        self.layout.addStretch()
        self.layout.addWidget(self.clear)
        self.layout.addWidget(self.quit)

        self.setLayout(self.layout)

        # self.description.textChanged[str].connect(self.check_disable)
        self.salary.textChanged[str].connect(self.check_disable)

    def clicked_connect(self, _send, _quit, _clear):
        self.send.clicked.connect(_send)
        self.quit.clicked.connect(_quit)
        self.clear.clicked.connect(_clear)

    @pyqtSlot()
    def check_disable(self):
        if not is_float(self.salary.text()):
            self.send.setEnabled(False)
        else:
            self.send.setEnabled(True)
