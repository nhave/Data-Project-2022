from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import uic, QtCore, QtGui

import sys

class WindowAdd(QMainWindow):
    def __init__(self, title):
        super(WindowAdd, self).__init__()
        uic.loadUi('ui/add.ui', self)
        self.setWindowTitle(title)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setFixedSize(400, 208)
        self.connectSignalSlots()
    
    def connectSignalSlots(self):
        self.buttonCalendar.clicked.connect(self.openCalendar)
        self.buttonDone.clicked.connect(self.done)
        self.buttonCancel.clicked.connect(self.close)
    
    def done(self):
        self.close()

    def openCalendar(self):
        self.windowdate = WindowDate(self)
        self.windowdate.show()

class WindowDate(QMainWindow):
    def __init__(self, parentWindow):
        super(WindowDate, self).__init__()
        uic.loadUi('ui/calendar.ui', self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setFixedSize(500, 400)
        self.connectSignalSlots()
        self.parentWindow = parentWindow
    
    def connectSignalSlots(self):
        self.buttonSet.clicked.connect(self.setDate)

    def setDate(self):
        date = self.calendar.selectedDate()
        day = str(date.getDate()[2])
        month = str(date.getDate()[1])
        year = str(date.getDate()[0])
        self.parentWindow.lineEditDate.setText(day + "-" + month + "-" + year)
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    winAdd = WindowAdd("Add")
    winAdd.show()

    sys.exit(app.exec())
