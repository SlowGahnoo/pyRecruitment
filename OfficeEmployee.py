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
    def __init__(self, l_amount, r_amount):
        super().__init__()

        print(l_amount)
        print(r_amount)
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("Employer index"))
        self.employer_index = QComboBox()
        self.employer_index.addItems([str(i) for i in range(l_amount)])
        self.layout.addWidget(self.employer_index)

        self.layout.addWidget(QLabel("Candidate index"))
        self.candidate_index = QComboBox()
        self.candidate_index.addItems([str(i) for i in range(r_amount)])
        self.layout.addWidget(self.candidate_index)

        self.send = QPushButton("Send recommendation")
        self.send.clicked.connect(self.match)
        self.quit = QPushButton("Quit")

        self.layout.addWidget(self.send)
        self.layout.addStretch()
        self.layout.addWidget(self.quit)
        self.setLayout(self.layout)

    def connect_lists(self, list1, list2, list3):
        self.jobs = list1
        self.candidates = list2
        self.requests = list3

    def match(self):
        id_work_pos = self.jobs[self.employer_index.currentIndex()]._id
        id_candidate = self.candidates[self.candidate_index.currentIndex()]._id
        request = self.requests[self.candidate_index.currentIndex()]
        dbman.matchCandidateJob(id_candidate, id_work_pos) 
        dbman.deleteRequest(request)
        dbman.commit()

class ListPanel(QWidget):
    def __init__(self, _type, _id):
        super().__init__()
        self.items = 0
        self.jobs = []
        self.candidates = []
        self.requests = []
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
                    self.jobs.append(j)
                    a = QListWidgetItem()
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
                    self.items += 1

        if self.type == "Request":
            requests = dbman.fetchOfficeRequests(self.usr_id)
            for i, r in enumerate(requests):
                c = dbman.fetchCandidate(r._id)
                if c.id_work_pos:
                    continue

                self.candidates.append(c)
                self.requests.append(r)

                card1 = CandidateCard([
                    c.name,
                    c.surname,
                    f"{c.street} {c.street_num}",
                    c.email,
                    "University"
                ])

                card2 = RequestCard([
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
                self.items += 1

    def getTotal(self):
        return self.items


class Widget(QWidget):
    def __init__(self, usr_id):
        super().__init__()
        self.usr_id = usr_id
        usr = dbman.fetchOfficeWorker(self.usr_id)

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel(f"Office worker - user {usr.name} {usr.surname}"))

        self.inner_layout = QHBoxLayout()

        self.left = ListPanel("Employer", self.usr_id)
        self.middle = ListPanel("Request", self.usr_id)
        self.right = RightPanel(self.left.getTotal(), self.middle.getTotal())

        self.inner_layout.addWidget(self.left)
        self.inner_layout.addWidget(self.middle)
        self.inner_layout.addWidget(self.right)
        self.layout.addLayout(self.inner_layout)
        self.right.connect_lists(self.left.jobs, self.middle.candidates, self.middle.requests)
        self.setLayout(self.layout)

        # self.right.clicked_connect(self.add_element, self.quit_application, self.clear_table)




    @pyqtSlot()
    def quit_application(self):
        QApplication.quit()

    @pyqtSlot()
    def clear_table(self):
        ret = QMessageBox().question(None, '',"Are you sure?", QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            self.list.clear()
            self.items = 0
