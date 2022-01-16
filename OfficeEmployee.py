from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSlot, QDate
from PyQt5.QtWidgets import *
from Cards import *

from DBManager import *

from util import *

dbman = DBManagement("test.db")


class Register(QWidget):
    def __init__(self, mainwindow):
        super().__init__()
        self.mainwindow = mainwindow
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

        self.layout.addWidget(QLabel("Phone number"))
        self.phone = QLineEdit()
        self.layout.addWidget(self.phone)


        self.layout.addStretch()

        self.register = QPushButton("Register")
        self.register.setEnabled(False)
        self.register.clicked.connect(self.register_user)
        self.layout.addWidget(self.register)

        self.fields = [
                self.usrname,
                self.passwd,
                self.cpasswd,
                self.name,
                self.surname,
                self.email,
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

    def register_user(self):
        usr_id = sum([ord(x) for x in self.email.text()])

        login = Login(
                    _id       = usr_id,
                    usrname   = self.usrname.text(), 
                    passwd    = self.passwd.text(), 
                    email     = self.email.text()
        )

        office_worker = OfficeWorker(
                _id       = usr_id,
                name      = self.name.text(),
                surname   = self.surname.text(),
                phone_num = self.phone.text(),
                email     = self.email.text(),
        )

        dbman.pushLogin(login)
        dbman.pushOfficeWorker(office_worker)
        dbman.commit()
        self.usr_id = usr_id
        self.mainwindow.switch_from_register()

    def getID(self):
        return self.usr_id


class RightPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.description = QPlainTextEdit()
        self.send = QPushButton("Send")
        self.clear = QPushButton("Clear")
        self.quit = QPushButton("Quit")
        self.send.setEnabled(False)

        self.location = QLineEdit()
        self.total_workers = QLineEdit()

        # Right
        self.layout = QVBoxLayout()


        self.layout.addWidget(self.send)
        self.layout.addStretch()
        self.layout.addWidget(self.clear)
        self.layout.addWidget(self.quit)

        self.setLayout(self.layout)

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

class ListPanel(QWidget):
    def __init__(self, _type, _id):
        super().__init__()
        self.items = 0
        self.type = _type
        self.usr_id = _id

        self.list = QListWidget()
        self.list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self.customContextMenuRequested)
        self.list.mouseReleaseEvent = self.listContext

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.list)
        self.fill_list()
        self.setLayout(self.layout)

    def listContext(self, event):
        if event.button() == QtCore.Qt.RightButton:
            menu = QMenu(self)
            edit = menu.addAction("Edit")
            delete = menu.addAction("Delete")
            details = menu.addAction("View details")
            action = menu.exec_(self.mapToGlobal(event.pos()))
            if action == delete:
                ret = QMessageBox().question(None, '',"Are you sure?", QMessageBox.Yes | QMessageBox.No)
                if ret == QMessageBox.Yes:
                    self.list.takeItem(self.list.indexAt(event.pos()).row())

    def fill_list(self):
        if self.type == "Employer":
            employers = dbman.fetchOfficeEmployerIDs(self.usr_id)
            for id_employer in employers:
                jobs = dbman.fetchJob(id_employer)
                for i, j in enumerate(jobs):
                    a = QListWidgetItem()
                    print(j)
                    card = JobCard([
                        j.domain,
                        j.description,
                        j.location,
                        j.company_name,
                        bool(j.telework),
                        j.total_workers,
                        float(j.salary),
                        j.submission_deadline
                    ])
                    a.setSizeHint(card.sizeHint())
                    self.list.addItem(a)
                    self.list.setItemWidget(a, card)
                    self.items = i

        if self.type == "Request":
            requests = dbman.fetchOfficeRequests(self.usr_id)
            for i, r in enumerate(requests):
                c = dbman.fetchCandidate(r._id)

                card1 = CandidateCard([
                    c.name,
                    c.surname,
                    f"{c.street} {c.street_num}",
                    c.email,
                    "University"
                ])

                card2 = JobCard([
                    float(r.desired_wage),
                    r.job_type,
                    bool(r.telework),
                    r.application_date
                ])
                a = QListWidgetItem()
                b = QListWidgetItem()

                a.setSizeHint(card1.sizeHint())
                self.list.addItem(a)
                self.list.setItemWidget(a, card1)

                b.setSizeHint(card2.sizeHint())
                self.list.addItem(b)
                self.list.setItemWidget(b, card2)
                self.items = i


    def add_element(self):
        a = QListWidgetItem()

        card = JobCard([])
        a.setSizeHint(card.sizeHint())
        self.list.addItem(a)

        self.list.setItemWidget(a, card)
        self.right.description.setPlainText("")
        self.right.salary.setText("")
        self.right.location.setText("")

        self.items += 1

class Widget(QWidget):
    def __init__(self, usr_id):
        super().__init__()
        self.usr_id = usr_id

        
        # self.right.clicked_connect(self.add_element, self.quit_application, self.clear_table)

        # self.fill_list()
        usr = dbman.fetchOfficeWorker(self.usr_id)
        QLabel(f"Office worker - user {usr.name} {usr.surname}")

        self.layout = QHBoxLayout(self)

        self.left = ListPanel("Employer", self.usr_id)
        self.middle = ListPanel("Request", self.usr_id)
        self.right = RightPanel()

        self.layout.addWidget(self.left)
        self.layout.addWidget(self.middle)
        self.layout.addWidget(self.right)

        self.setLayout(self.layout)




    @pyqtSlot()
    def quit_application(self):
        QApplication.quit()

    @pyqtSlot()
    def clear_table(self):
        ret = QMessageBox().question(None, '',"Are you sure?", QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            self.list.clear()
            self.items = 0
