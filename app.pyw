import sys, os, platform, json, time

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QSplashScreen, QFileDialog
)
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap
from pathlib import Path
from config import Config
from language import Lang

rows = ["table.package", "table.content", "table.amount", "table.date"]
packages = []

class WindowMain(QMainWindow):
    def __init__(self):
        super(WindowMain, self).__init__()
        uic.loadUi(resourcePath('assets/ui/mainwindow.ui'), self)
        self.setWindowIcon(QtGui.QIcon(resourcePath('assets/textures/icon.ico')))
        self.connectSignalsSlots()
        self.updateItems()
        self.resize(800, 600)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.localize()

    def connectSignalsSlots(self):
        # Link Events to their methods.
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.about)
        self.actionExport.triggered.connect(self.exportItems)
        self.actionImport.triggered.connect(self.importItems)
        self.actionSave.triggered.connect(self.saveItems)
        self.actionAdd.triggered.connect(self.addItem)
        self.actionEdit.triggered.connect(self.editItem)
        self.actionRemove.triggered.connect(self.removeItem)
        self.actionPreferences.triggered.connect(self.openPreferences)
        # Adding the Context Menu and its Event.
        self.tableItems.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableItems.customContextMenuRequested.connect(self.contextMenu)

    def contextMenu(self, pos):
        index = self.tableItems.indexAt(pos)
        if(index.isValid()):
            self.contextMenu = QtWidgets.QMenu(self)
            EditAction = QtWidgets.QAction(lang.translate("context.edit"), self)
            removeAction = QtWidgets.QAction(lang.translate("context.remove"), self)
            EditAction.triggered.connect(self.editItem)
            removeAction.triggered.connect(self.removeItem)
            self.contextMenu.addAction(EditAction)
            self.contextMenu.addAction(removeAction)
            self.contextMenu.popup(QtGui.QCursor.pos())

    def about(self):
        QMessageBox.about(
            self,
            lang.translate("main.title"),
            lang.translate("about.desc") +
            lang.translate("about.version") + ": 1.0.0<br>" +
            lang.translate("about.author") + ": NHAVE<br>"
            "<a href='https://github.com/nhave/Data-Project-2022'>Github</a>"
        )

    def addItem(self):
        self.windowAdd = WindowAdd(self, False)
        self.windowAdd.show()

    def editItem(self):
        self.windowAdd = WindowAdd(self, True)
        self.windowAdd.show()

    def removeItem(self):
        row = self.tableItems.currentItem().row()

        msg = ""
        for i in range(len(rows)):
            msg += "<br>" + lang.translate(rows[i]) + ": " + packages[row][i]
            pass

        reply = QMessageBox.critical(self, lang.translate("windowremove.title"),
        lang.translate("windowremove.message") + msg, 
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No)

        if reply == QMessageBox.Yes:
            if(len(packages) > 0):
                packages.pop(row)
                self.updateItems()

    def updateItems(self):
        _translate = QtCore.QCoreApplication.translate
        self.tableItems.setColumnCount(len(rows))
        self.tableItems.setRowCount(len(packages))

        for row in range(len(rows)):
            item = QtWidgets.QTableWidgetItem()
            item.setText(lang.translate(rows[row]))
            self.tableItems.setHorizontalHeaderItem(row, item)

        for row in range(len(packages)):
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(row + 1))
            self.tableItems.setVerticalHeaderItem(row, item)
            for column in range(len(packages[row])):
                item = QtWidgets.QTableWidgetItem()
                item.setText(packages[row][column])
                self.tableItems.setItem(row, column, item)
        
        if(self.tableItems.currentItem() == None):
            self.tableItems.selectRow(0)
        self.actionRemove.setEnabled(len(packages) > 0)
        self.actionEdit.setEnabled(len(packages) > 0)

    def exportItems(self):
        filename, ok = QFileDialog.getSaveFileName(
            self,
            lang.translate("file.export"),
            "./",
            "Database (*.NTDB)"
        )
        if filename:
            path = Path(filename)
            config.setString("last_file", filename)
            config.save()
            with open(path, 'w', encoding='utf8') as json_file:
                json.dump(packages, json_file, sort_keys=True, ensure_ascii=False)
    
    def saveItems(self):
        filename = config.getString("last_file", "")
        path = Path(filename)
        if not path.is_file() or not filename.lower().endswith(".ntdb"):
            self.exportItems()
            return

        config.setString("last_file", filename)
        config.save()
        with open(path, 'w', encoding='utf8') as json_file:
            json.dump(packages, json_file, sort_keys=True, ensure_ascii=False)

    def importItems(self):
        global packages

        filename, ok = QFileDialog.getOpenFileName(
            self,
            lang.translate("file.import"),
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

    def openPreferences(self):
        self.windowPreferences = WindowPreferences(self)
        self.windowPreferences.show()

    def localize(self):
        self.setWindowTitle(lang.translate("windowmain.title"))

        self.menuFile.setTitle(lang.translate("menu.file"))
        self.menuEdit.setTitle(lang.translate("menu.edit"))
        self.menuInfo.setTitle(lang.translate("menu.info"))

        self.actionExit.setText(lang.translate("context.exit"))
        self.actionAbout.setText(lang.translate("context.about"))
        self.actionExport.setText(lang.translate("context.export"))
        self.actionImport.setText(lang.translate("context.import"))
        self.actionSave.setText(lang.translate("context.save"))
        self.actionAdd.setText(lang.translate("context.add"))
        self.actionEdit.setText(lang.translate("context.edit"))
        self.actionRemove.setText(lang.translate("context.remove"))
        self.actionPreferences.setText(lang.translate("context.preferences"))

class WindowAdd(QMainWindow):
    def __init__(self, parentWindow, edit):
        super(WindowAdd, self).__init__()
        self.parentWindow = parentWindow
        uic.loadUi(resourcePath('assets/ui/add.ui'), self)
        self.setWindowIcon(QtGui.QIcon(resourcePath('assets/textures/icon.ico')))
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setFixedSize(400, 200)
        self.connectSignalSlots()
        self.updateLines(edit)
        self.localize(edit)
    
    def connectSignalSlots(self):
        self.buttonCalendar.clicked.connect(self.openCalendar)
        self.buttonDone.clicked.connect(self.done)
        self.buttonCancel.clicked.connect(self.close)

    def updateLines(self, edit):
        self.edit = edit
        if edit:
            row = self.parentWindow.tableItems.currentItem().row()
            self.lineEditID.setText(packages[row][0])
            self.lineEditContent.setText(packages[row][1])
            self.lineEditAmount.setText(packages[row][2])
            self.lineEditDate.setText(packages[row][3])
    
    def done(self):
        id = self.lineEditID.text()
        content = self.lineEditContent.text()
        amount = self.lineEditAmount.text()
        date = self.lineEditDate.text()

        if len(id) < 1 or len(content) < 1 or len(amount) < 1 or len(date) < 1:
            reply = QMessageBox.critical(self, lang.translate("windowerror.title"),
            lang.translate("windowerror.message"), 
            QMessageBox.Ok)

            if reply == QMessageBox.Ok:
                return

        if not self.edit:
            packages.append([id, content, amount, date])
        else:
            row = self.parentWindow.tableItems.currentItem().row()
            packages[row] = [id, content, amount, date]

        self.parentWindow.updateItems()
        if not self.edit:
            self.parentWindow.tableItems.selectRow(len(packages)-1)
        self.close()

    def openCalendar(self):
        self.windowdate = WindowDate(self)
        self.windowdate.show()
        
    def localize(self, edit):
        title = lang.translate("context.add")
        if edit:
            title = lang.translate("context.edit")
        self.setWindowTitle(title)

        self.labelID.setText(lang.translate(rows[0]))
        self.labelContent.setText(lang.translate(rows[1]))
        self.labelAmount.setText(lang.translate(rows[2]))
        self.labelDate.setText(lang.translate(rows[3]))

        self.buttonDone.setText(lang.translate("button.done"))
        self.buttonCancel.setText(lang.translate("button.cancel"))
        self.buttonCalendar.setText(lang.translate("button.calendar"))

class WindowDate(QMainWindow):
    def __init__(self, parentWindow):
        super(WindowDate, self).__init__()
        self.parentWindow = parentWindow
        uic.loadUi(resourcePath('assets/ui/calendar.ui'), self)
        self.setWindowIcon(QtGui.QIcon(resourcePath('assets/textures/icon.ico')))
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setFixedSize(500, 400)
        self.connectSignalSlots()
        self.localize()
    
    def connectSignalSlots(self):
        self.buttonSet.clicked.connect(self.setDate)

    def setDate(self):
        date = self.calendar.selectedDate()
        day = str(date.getDate()[2])
        month = str(date.getDate()[1])
        year = str(date.getDate()[0])
        self.parentWindow.lineEditDate.setText(day + "-" + month + "-" + year)
        self.close()

    def localize(self):
        self.setWindowTitle(lang.translate("windowcalendar.title"))
        self.buttonSet.setText(lang.translate("button.set"))

class WindowPreferences(QMainWindow):
    def __init__(self, parentWindow):
        super(WindowPreferences, self).__init__()
        self.parentWindow = parentWindow
        uic.loadUi(resourcePath('assets/ui/preferences.ui'), self)
        self.setWindowIcon(QtGui.QIcon(resourcePath('assets/textures/icon.ico')))
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setFixedSize(400, 200)
        self.connectSignalSlots()
        self.localize()
        self.updateItem()
    
    def connectSignalSlots(self):
        self.buttonDone.clicked.connect(self.done)
        self.comboBoxLang.activated.connect(self.comboBox)
    
    def updateItem(self):
        # test = QtWidgets.QComboBox()
        # test.setCurrentIndex
        self.labelLangChange.hide()
        langs = lang.listLanguages()
        for i in range(len(langs)):
            self.comboBoxLang.addItem(langs[i][1])
            if langs[i][0] == current_lang:
                self.comboBoxLang.setCurrentIndex(i)
    
    def comboBox(self):
        index = self.comboBoxLang.currentIndex()
        langs = lang.listLanguages()
        if langs[index][0] == current_lang:
            self.labelLangChange.hide()
        else:
            self.labelLangChange.show()
        config.setString("current_lang", langs[index][0])
    
    def done(self):
        config.save()
        self.close()
    
    def localize(self):
        self.setWindowTitle(lang.translate("windowpreferences.title"))
        self.labelLanguage.setText(lang.translate("settings.language"))
        self.labelLangChange.setText(lang.translate("settings.langchange"))
        self.buttonDone.setText(lang.translate("button.done"))

# Returns the resource path for assets for use in the EXE file.
def resourcePath(relativePath):
    try:
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")
    
    return os.path.join(basePath, relativePath)

# Defines the config location based on the OS used.
def getConfigLocation():
    _os = platform.system()
    if (_os == "Linux"):
        return os.getenv('HOME') + "/.ntech/ntpkg/"
    elif (_os == "Windows"):
        return os.getenv('APPDATA') + "/N-TECH/NTPKG/"
    return "./"

# Only run if this is the main class
if __name__ == "__main__":
    config = Config(getConfigLocation() + "conf.json")
    last_file = config.getString("last_file", "")
    current_lang = config.getString("current_lang", "en_us")
    config.save()

    lang = Lang(resourcePath('assets/lang/lang.json'), current_lang)

    try:
        with open(last_file, 'r', encoding='utf8') as f:
            file = json.load(f)
            if type(file) == list:
                packages = file
    except:
        pass

    app = QApplication(sys.argv)

    splashPixmap = QPixmap(resourcePath("assets/textures/splash.png"))
    splash = QSplashScreen(splashPixmap, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splashPixmap.mask())

    splash.show()
    time.sleep(1)

    win = WindowMain()
    win.show()

    splash.finish(win)

    sys.exit(app.exec())