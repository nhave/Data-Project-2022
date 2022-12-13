import sys, os, platform, json, time

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QSplashScreen, QFileDialog
)
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap
from pathlib import Path
from config import Config

# from ui_mainwindow import Ui_MainWindow

rows = ["Package ID", "Content", "Amount", "Date"]
packages = []

class WindowMain(QMainWindow):
    def __init__(self):
        super(WindowMain, self).__init__()
        uic.loadUi(resourcePath('mainwindow.ui'), self)
        self.setWindowIcon(QtGui.QIcon(resourcePath('icon.ico')))
        # self.setupUi(self)
        self.connectSignalsSlots()
        self.updateItems()
        self.resize(800, 600)
        
        self.setWindowState(QtCore.Qt.WindowMaximized)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def connectSignalsSlots(self):
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.about)
        self.actionExport.triggered.connect(self.exportItems)
        self.actionImport.triggered.connect(self.importItems)
        self.actionAdd.triggered.connect(self.addItem)
        self.actionEdit.triggered.connect(self.editItem)
        self.actionRemove.triggered.connect(self.removeItem)

    def about(self):
        QMessageBox.about(
            self,
            "N-TECH Package Manager",
            "<p>Et concept af et program til at registrere pakker.</p>"
            "Version: 1.0.0<br>"
            "Authors: NHAVE, Uno<br>"
            "<a href='https://github.com/nhave/Data-Project-2022'>Github</a>"
        )

    def addItem(self):
        # packages.append(["ID", "Pakke", "Antal", "Dato"])
        # self.updateItems()
        self.windowadd = WindowAdd(False)
        self.windowadd.show()

    def editItem(self):
        # packages.append(["ID", "Pakke", "Antal", "Dato"])
        # self.updateItems()
        self.windowadd = WindowAdd(True)
        self.windowadd.show()

    def removeItem(self):
        # if(len(packages) > 0):
        #     packages.pop(len(packages) -1)
        #     self.updateItems()
        pass

    def updateItems(self):
        _translate = QtCore.QCoreApplication.translate
        self.tableItems.setColumnCount(len(rows))
        self.tableItems.setRowCount(len(packages))

        for row in range(len(rows)):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate("MainWindow", rows[row]))
            self.tableItems.setHorizontalHeaderItem(row, item)

        for row in range(len(packages)):
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(row + 1))
            self.tableItems.setVerticalHeaderItem(row, item)
            for column in range(len(packages[row])):
                item = QtWidgets.QTableWidgetItem()
                item.setText(packages[row][column])
                self.tableItems.setItem(row, column, item)

    def exportItems(self):
        filename, ok = QFileDialog.getSaveFileName(
            self,
            "Export Database",
            "./",
            "Database (*.NTDB)"
        )
        if filename:
            path = Path(filename)
            config.setString("last_file", filename)
            config.save()
            with open(path, 'w', encoding='utf8') as json_file:
                json.dump(packages, json_file, sort_keys=True, ensure_ascii=False)
    
    def importItems(self):
        global packages

        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Import Database",
            "./",
            "Database (*.NTDB)"
        )
        if filename:
            path = Path(filename)
            config.setString("last_file", filename)
            config.save()
            try:
                with open(path, 'r', encoding='utf8') as f:
                    file = json.load(f)
                    if type(file) == list:
                        packages = file
                        self.updateItems()
            except:
                pass

        # try:
        #     with open("test.dat", 'r', encoding='utf8') as f:
        #         conf = json.load(f)
        #         if type(conf) == list:
        #             packages = conf
        #             self.updateItems()
        # except:
        #     pass

class WindowAdd(QMainWindow):
    def __init__(self, edit):
        super(WindowAdd, self).__init__()
        uic.loadUi(resourcePath('add.ui'), self)
        self.setWindowIcon(QtGui.QIcon(resourcePath('icon.ico')))
        title = "Add"
        if edit:
            title = "Edit"
        self.setWindowTitle(title)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setFixedSize(400, 208)
        self.connectSignalSlots()

        self.edit = edit
    
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
        uic.loadUi(resourcePath('calendar.ui'), self)
        self.setWindowIcon(QtGui.QIcon(resourcePath('icon.ico')))
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

def resourcePath(relativePath):
    try:
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")
    
    return os.path.join(basePath, relativePath)

def getConfigLocation():
    _os = platform.system()
    if (_os == "Linux"):
        return os.getenv('HOME') + "/.ntech/ntpkg/"
    elif (_os == "Windows"):
        return os.getenv('APPDATA') + "/N-TECH/NTPKG/"
    return "./"

if __name__ == "__main__":
    config = Config(getConfigLocation() + "conf.json")
    last_file = config.getString("last_file", "")
    config.save()

    try:
        with open(last_file, 'r', encoding='utf8') as f:
            file = json.load(f)
            if type(file) == list:
                packages = file
    except:
        pass

    app = QApplication(sys.argv)

    splashPixmap = QPixmap(resourcePath("splash.png"))
    splash = QSplashScreen(splashPixmap, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splashPixmap.mask())

    splash.show()
    time.sleep(1)

    win = WindowMain()
    win.show()

    splash.finish(win)

    sys.exit(app.exec())