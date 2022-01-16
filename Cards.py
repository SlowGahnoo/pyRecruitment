from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

import os.path
basedir = os.path.dirname(os.path.realpath(__file__))

class CardWidget(QWidget):
    def __init__(self, fields, data, icon_path: str):
        super().__init__()
        self.layout = QHBoxLayout()
        self.left = QVBoxLayout()
        self.right = QVBoxLayout()

        self.icon = QLabel()
        self.icon.setPixmap(QPixmap(os.path.join(basedir, icon_path)))
        self.icon.setFixedWidth(67)
        self.layout.addWidget(self.icon)

        d = [QLabel(s.format(f)) for s, f in zip(fields, data)]
        [q.setWordWrap(True) for q in d]
        left  = d[:len(d)//2]
        right = d[len(d)//2:]

        for l in left:
            self.left.addWidget(l)

        for r in right:
            self.right.addWidget(r)

        self.layout.addLayout(self.left)
        self.layout.addLayout(self.right)
        self.setLayout(self.layout)

class CandidateCard(CardWidget):
    def __init__(self, data):
        fields = ["<b><u>Name</u></b>: {}",
                  "<b><u>Surname</u></b>: {}",
                  "<b><u>Address</u></b>: {}",
                  "<b><u>Email</u></b>: {}",
                  "<b><u>Graduated</u></b>: {}",
        ]
        icon_path = "assets/r_person.png"
        super().__init__(fields, data, icon_path)

class RequestCard(CardWidget):
    def __init__(self, data):
        fields = [
                "<b><u>Desired Salary:</b></u> {:.2f} € / month",
                "<b><u>Work Type:</b></u> {}",
                "<b><u>Remote:</b></u> {}",
                "<b><u>Application date:</b></u> {}",
        ]
        icon_path = "assets/r_person.png"
        super().__init__(fields, data, icon_path)

class JobCard(CardWidget):
    def __init__(self, data):
        fields = [
                "<b><u>Description</u></b>:\n{}",
                "<b><u>Location</u></b>:\n{}",
                "<b><u>Salary</u></b>:\n{:.2f} € / month",
                "<b><u>Submission Deadline</u></b>:\n{}"
                # "<b><u></u></b>"
        ]
        icon_path = "assets/r_case.png"
        super().__init__(fields, data, icon_path)
