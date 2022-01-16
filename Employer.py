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

        self.layout.addWidget(QLabel("Company Name"))
        self.company = QLineEdit()
        self.layout.addWidget(self.company)

        self.layout.addWidget(QLabel("Company Location"))
        self.location = QLineEdit()
        self.layout.addWidget(self.location)

        self.layout.addWidget(QLabel("Est Date"))


        self.est_date = QDateEdit()
        self.est_date.setDisplayFormat("yyyy")
        self.layout.addWidget(self.est_date)

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

    def register_user(self):
        usr_id = sum([ord(x) for x in self.email.text()])
        company_id = sum([ord(x) for x in self.company.text() + self.location.text()])

        login = Login(
                    _id     = usr_id,
                    usrname = self.name.text(), 
                    passwd  = self.passwd.text(), 
                    email   = self.email.text()
        )

        employer = Employer(
                _id          = usr_id,
                name         = self.name.text(), 
                surname      = self.surname.text(), 
                email        = self.email.text(),
                phone_num    = self.phone.text(), 
                company_name = self.company.text(),
                id_company   = company_id
        )

        company = Company(
                _id      = company_id,
                name     = self.company.text(),
                location = self.location.text(),
                est_date = self.est_date.date().toString("yyyy")
                )

        dbman.pushEmployer(employer)
        dbman.pushCompany(company)
        dbman.pushLogin(login)
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

        self.salary = QLineEdit()
        self.location = QLineEdit()
        self.total_workers = QLineEdit()

        # Right
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("Location"))
        self.layout.addWidget(self.location)
        self.layout.addWidget(QLabel("Salary"))
        self.layout.addWidget(self.salary)

        self.layout.addWidget(QLabel("Total workers"))
        self.layout.addWidget(self.total_workers)

        self.layout.addWidget(QLabel("Description"))
        self.layout.addWidget(self.description)

        self.telework = QCheckBox()
        self.telework.setText("Telework")
        self.layout.addWidget(self.telework)

        domain = dbman.fetchSpecialties()
        self.layout.addWidget(QLabel("Domain/Specialty"))
        self.domain = QComboBox()
        self.domain.addItems(domain)

        self.layout.addWidget(self.domain)

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

class Widget(QWidget):
    def __init__(self, usr_id):
        super().__init__()
        self.usr_id = usr_id
        self.items = 0

        self.list = QListWidget()
        self.list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self.customContextMenuRequested)
        self.list.mouseReleaseEvent = self.listContext
        
        self.right = RightPanel()
        self.right.clicked_connect(self.add_element, self.quit_application, self.clear_table)

        self.fill_list()

        self.layout = QHBoxLayout(self)

        self.left = QVBoxLayout()
        usr = dbman.fetchEmployer(self.usr_id)
        self.company = usr.company_name
        self.left.addWidget(QLabel(f"Jobs - user {usr.name} {usr.surname}"))
        self.left.addWidget(self.list)
        self.layout.addLayout(self.left)
        self.layout.addWidget(self.right)

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

    def fill_list(self, data = None):
        jobs = dbman.fetchJob(self.usr_id)
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

    def add_element(self):
        a = QListWidgetItem()
        card = JobCard([
            self.right.domain.currentText(),
            self.right.description.toPlainText(), 
            self.right.location.text(), 
            self.company,
            bool(self.right.telework.isChecked()),
            self.right.total_workers.text(),
            float(self.right.salary.text()), 
            self.right.calendar.selectedDate().toString("yyyy-MM-dd")
        ])

        job = Job(
            domain = self.right.domain.currentIndex() + 1,
            description = self.right.description.toPlainText(), 
            location = self.right.location.text(), 
            company_name = self.company,
            telework = int(self.right.telework.isChecked()),
            total_workers = self.right.total_workers.text(),
            salary = self.right.salary.text(), 
            submission_deadline = self.right.calendar.selectedDate().toString("yyyy-MM-dd"),
            id_employer = self.usr_id
        )

        dbman.pushJob(job)
        dbman.commit()

        a.setSizeHint(card.sizeHint())
        self.list.addItem(a)

        self.list.setItemWidget(a, card)
        self.right.description.setPlainText("")
        self.right.salary.setText("")
        self.right.location.setText("")

        self.items += 1

    @pyqtSlot()
    def quit_application(self):
        QApplication.quit()

    @pyqtSlot()
    def clear_table(self):
        ret = QMessageBox().question(None, '',"Are you sure?", QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            self.list.clear()
            self.items = 0
