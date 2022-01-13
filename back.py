from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtChart import QChartView, QPieSeries, QChart
from PyQt5.QtGui import QPainter

# import signal
# signal.signal(signal.SIGINT, signal.SIG_DFL)

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.items = 0
        self._data = {"Water": 24.5, "Electricity": 55.1, "Rent": 850.0,
                "Supermarket": 230.4, "Internet": 29.99, "Bars": 21.85}

        # Left
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Description", "Price"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Chart
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # Right
        self.description = QLineEdit()
        self.price = QLineEdit()
        self.add = QPushButton("Add")
        self.clear = QPushButton("Clear")
        self.quit = QPushButton("Quit")
        self.plot = QPushButton("Plot")

        self.add.setEnabled(False)

        self.right = QVBoxLayout()
        self.right.addWidget(QLabel("Description"))
        self.right.addWidget(self.description)
        self.right.addWidget(QLabel("Price"))
        self.right.addWidget(self.price)
        self.right.addWidget(self.add)
        self.right.addWidget(self.plot)
        self.right.addWidget(self.chart_view)
        # self.right.addStretch()
        self.right.addWidget(self.clear)
        self.right.addWidget(self.quit)

        self.right.addWidget(self.plot)


        self.add.clicked.connect(self.add_element)
        self.quit.clicked.connect(self.quit_application)
        self.clear.clicked.connect(self.clear_table)
        self.plot.clicked.connect(self.plot_data)

        self.description.textChanged[str].connect(self.check_disable)
        self.price.textChanged[str].connect(self.check_disable)

        self.fill_table()

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.right)

        self.setLayout(self.layout)

    @pyqtSlot()
    def plot_data(self):
        series = QPieSeries()
        for i in range(self.table.rowCount()):
            text = self.table.item(i, 0).text()
            number = float(self.table.item(i, 1).text())
            series.append(text, number)

        chart = QChart()
        chart.addSeries(series)
        chart.legend().setAlignment(QtCore.Qt.AlignLeft)
        self.chart_view.setChart(chart)

    def add_element(self):
        des = self.description.text()
        price = self.price.text()

        self.table.insertRow(self.items)
        self.table.setItem(self.items, 0, QTableWidgetItem(des))
        self.table.setItem(self.items, 1, QTableWidgetItem(price))

        self.description.setText("")
        self.price.setText("")
        self.items += 1

    @pyqtSlot()
    def quit_application(self):
        QApplication.quit()

    @pyqtSlot()
    def clear_table(self):
        self.table.setRowCount(0)
        self.items = 0

    def fill_table(self, data = None):
        data = self._data if not data else data
        for i, (desc, price) in enumerate(data.items()):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(desc))
            self.table.setItem(i, 1, QTableWidgetItem(str(price)))
            self.items = i

    @pyqtSlot()
    def check_disable(self):
        if not self.description.text() or not self.price.text():
            self.add.setEnabled(False)
        else:
            self.add.setEnabled(True)


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


import DBManager
d = DBManager.DBManagement("test.db")
def main():
    app = QApplication([])
    print(d)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    return app.exec()
