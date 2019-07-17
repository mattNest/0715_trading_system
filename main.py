from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import *

import sys,sqlite3,time
import os

class InsertDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(InsertDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Add Strategy")

        self.setWindowTitle("Trading Strategy Upload")
        self.setFixedWidth(300)
        self.setFixedHeight(250)

        self.QBtn.clicked.connect(self.addstudent)

        layout = QVBoxLayout()

        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Strategy Name")
        layout.addWidget(self.nameinput)

        self.branchinput = QComboBox()
        self.branchinput.addItem("順勢策略")
        self.branchinput.addItem("逆勢策略")
        layout.addWidget(self.branchinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def addstudent(self):

        name = ""
        branch = ""

        name = self.nameinput.text()
        branch = self.branchinput.itemText(self.branchinput.currentIndex())
        
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            self.c.execute("INSERT INTO strategy (name,branch) VALUES (?,?)",(name,branch))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Successful','Strategy is added successfully to the database.')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not add strategy to the database.')

class SearchDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Search")

        self.setWindowTitle("Search Strategy")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.search_strategy)
        layout = QVBoxLayout()

        self.searchinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.searchinput.setValidator(self.onlyInt)
        self.searchinput.setPlaceholderText("Trading Strategy No.")
        layout.addWidget(self.searchinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def search_strategy(self):

        searchrol = ""
        searchrol = self.searchinput.text()
        
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            result = self.c.execute("SELECT * from strategy WHERE roll="+str(searchrol))
            row = result.fetchone()
            serachresult = "Strategy No. : " + str(row[0]) + '\n' + "Name : " + str(row[1]) + '\n' + "Branch : " + str(row[2])
            QMessageBox.information(QMessageBox(), 'Successful', serachresult)
            self.conn.commit()
            self.c.close()
            self.conn.close()
        
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Cannot find strategy from db.')

class DeleteDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(DeleteDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Delete")

        self.setWindowTitle("Delete Strategy")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.deletestudent)
        layout = QVBoxLayout()

        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("Strategy No.")
        layout.addWidget(self.deleteinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deletestudent(self):

        delrol = ""
        delrol = self.deleteinput.text()
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            self.c.execute("DELETE FROM strategy WHERE roll="+str(delrol))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Successful','Deleted From Table Successful')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not Delete strategy from the database.')

class LoginDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(LoginDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(500)
        self.setFixedHeight(120)

        layout = QVBoxLayout()

        self.passinput = QLineEdit()
        self.passinput.setEchoMode(QLineEdit.Password)
        self.passinput.setPlaceholderText("Enter Password.")
        self.QBtn = QPushButton()
        self.QBtn.setText("Login and Chill")
        self.setWindowTitle('Login')
        self.QBtn.clicked.connect(self.login)

        title = QLabel("Welcome, Bincentive's Greatest Quantative Analyst")
        font = title.font()
        font.setPointSize(16)
        title.setFont(font)

        layout.addWidget(title)
        layout.addWidget(self.passinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def login(self):
        if(self.passinput.text() == "root"):
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Wrong Password')

class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(300)
        self.setFixedHeight(250)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("Bincentive Trading Team")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        labelpic = QLabel()

        now_path = os.getcwd() # get the path now
        icon_path = os.path.join(now_path,'icon')
        logo_path = os.path.join(icon_path, 'logo.png')
        pixmap = QPixmap(logo_path)
        
        pixmap = pixmap.scaledToWidth(275)
        labelpic.setPixmap(pixmap)
        labelpic.setFixedHeight(150)

        layout.addWidget(title)

        # github info
        layout.addWidget(QLabel("github: github.com/mattNest"))
        layout.addWidget(QLabel("Created by Matthew"))
        layout.addWidget(labelpic)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

class RunStrategyDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(RunStrategyDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Run")

        self.setWindowTitle("Run Strategy")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.run_strategy)
        layout = QVBoxLayout()

        self.searchinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.searchinput.setValidator(self.onlyInt)
        self.searchinput.setPlaceholderText("Trading Strategy No.")
        layout.addWidget(self.searchinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def run_strategy(self):

        strategy_number = ""
        strategy_number = self.searchinput.text() # get the input strategy number from the user
        
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            result = self.c.execute("SELECT * from strategy WHERE roll="+str(strategy_number))
            row = result.fetchone()
            serachresult = "Strategy No. : " + str(row[0]) + '\n' + "Name : " + str(row[1]) + '\n' + "Branch : " + str(row[2])
            QMessageBox.information(QMessageBox(), 'Successful', serachresult)
            self.conn.commit()
            self.c.close()
            self.conn.close()
            

            # run the strategy
            py_path_now_initial = os.getcwd()
            py_path_now = os.path.join(py_path_now_initial,'test_code', str(strategy_number))
            os.chdir(py_path_now) # change the directory to the .py file folder
            print(os.system("ls"))
            os.system("python test_1.py") # run the strategy command
            os.chdir(py_path_now_initial) # change the directory back to the original path

        
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Cannot find strategy from db.')

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS strategy(roll INTEGER PRIMARY KEY AUTOINCREMENT ,name TEXT,branch TEXT)")
        self.c.close()

        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&About")
        self.setWindowTitle("Trading Strategy Management System")
        self.setMinimumSize(800, 600)

        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("Strategy No.", "Name", "Branch"))


        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        now_path = os.getcwd()
        icon_path = os.path.join(now_path,'icon')
        add_png_path = os.path.join(icon_path,'add.png')
        btn_ac_adduser = QAction(QIcon(add_png_path), "Add Strategy", self)
        btn_ac_adduser.triggered.connect(self.insert)
        btn_ac_adduser.setStatusTip("Add Strategy")
        toolbar.addAction(btn_ac_adduser)

        refresh_png_path = os.path.join(icon_path,'refresh.png')
        btn_ac_refresh = QAction(QIcon(refresh_png_path),"Refresh",self)
        btn_ac_refresh.triggered.connect(self.loaddata)
        btn_ac_refresh.setStatusTip("Refresh Table")
        toolbar.addAction(btn_ac_refresh)

        search_png_path = os.path.join(icon_path,'search.png')
        btn_ac_search = QAction(QIcon(search_png_path), "Search", self)
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Search Strategy")
        toolbar.addAction(btn_ac_search)

        trash_png_path = os.path.join(icon_path,'trash.png')
        btn_ac_delete = QAction(QIcon(trash_png_path), "Delete", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Delete Strategy")
        toolbar.addAction(btn_ac_delete)

        adduser_action = QAction(QIcon(add_png_path),"Insert Strategy", self)
        adduser_action.triggered.connect(self.insert)
        file_menu.addAction(adduser_action)

        searchuser_action = QAction(QIcon(search_png_path), "Search Strategy", self)
        searchuser_action.triggered.connect(self.search)
        file_menu.addAction(searchuser_action)

        deluser_action = QAction(QIcon(trash_png_path), "Delete", self)
        deluser_action.triggered.connect(self.delete)
        file_menu.addAction(deluser_action)

        info_png_path = os.path.join(icon_path,'info.png')
        about_action = QAction(QIcon(info_png_path),"Developer", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        go_png_path = os.path.join(icon_path,'go.png')
        trigger_strategy = QAction(QIcon(go_png_path), "Run", self)
        trigger_strategy.triggered.connect(self.run)
        toolbar.addAction(trigger_strategy)

    def loaddata(self): # draw the main table
        self.connection = sqlite3.connect("database.db")
        query = "SELECT * FROM strategy"
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        self.connection.close()

    def handlePaintRequest(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        model = self.table.model()
        table = cursor.insertTable(
            model.rowCount(), model.columnCount())
        for row in range(table.rows()):
            for column in range(table.columns()):
                cursor.insertText(model.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)
        document.print_(printer)

    def insert(self):
        dlg = InsertDialog()
        dlg.exec_()

    def delete(self):
        dlg = DeleteDialog()
        dlg.exec_()

    def search(self):
        dlg = SearchDialog()
        dlg.exec_()

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def run(self):
        dlg = RunStrategyDialog()
        dlg.exec_()


app = QApplication(sys.argv)
passdlg = LoginDialog()
if(passdlg.exec_() == QDialog.Accepted):
    window = MainWindow()
    window.show()
    window.loaddata()


sys.exit(app.exec_())