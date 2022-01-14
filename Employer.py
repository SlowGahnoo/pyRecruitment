from PyQt5.QtCore import QObject, pyqtSlot, QDate
from PyQt5.QtWidgets import *

class Register(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Employer Register Screen")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

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
