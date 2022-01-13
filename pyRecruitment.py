from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject, pyqtSlot, QDate

from Cards import *
import Employer

def is_float(n):
    try:
        float(n)
        return True
    except ValueError:
        return False


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.items = 0

        self.list = QListWidget()
        self.list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self.customContextMenuRequested)
        self.list.mouseReleaseEvent = self.listContext
        
        self.right = Employer.RightPanel()
        self.right.clicked_connect(self.add_element, self.quit_application, self.clear_table)

        self.fill_list()

        self.layout = QHBoxLayout(self)

        self.left = QVBoxLayout()
        self.left.addWidget(QLabel("Placeholder text"))
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
        data = 5*[(0, 0)] 
        for i, (desc, price) in enumerate(data):
            a = QListWidgetItem()
            card = JobCard(["N/A", "N/A", 0, "N/A", "N/A"])
            a.setSizeHint(card.sizeHint())
            self.list.addItem(a)
            self.list.setItemWidget(a, card)
            self.items = i

    def add_element(self):
        a = QListWidgetItem()
        card = JobCard([
            self.right.description.toPlainText(), 
            self.right.location.text(), 
            float(self.right.salary.text()), 
            self.right.calendar.selectedDate().toString(QtCore.Qt.DefaultLocaleLongDate)
        ])

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_app)
        self.file_menu.addAction(exit_action)

        self.setCentralWidget(Widget())

    @pyqtSlot()
    def exit_app(self, checked = None):
        print("Exited")
        QApplication.quit()


# d = DBManagement("test.db")
def main():
    app = QApplication([])
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    return app.exec()
