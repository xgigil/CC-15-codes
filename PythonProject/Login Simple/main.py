import sys
import mysql.connector
from PyQt6.QtSql import password
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from mysql.connector import Error
from login_ui import Ui_MainWindow

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.loginButton.clicked.connect(self.login_account)

    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="users"
            )
            if connection.is_connected():
                return connection
        except Error as e:
            self.statusLabel.setText(f"Error: {e}")
            return None

    def login_account(self):
        pass


app = QApplication([])
window = MyApp()
window.show()
app.exec()
