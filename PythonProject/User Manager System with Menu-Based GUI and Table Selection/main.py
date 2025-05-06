import sys
import mysql.connector
from mysql.connector import Error
from PyQt6.QtWidgets import QApplication, QMenuBar, QMainWindow, QLineEdit, QPushButton, \
    QLabel, QTableWidget, QWidget, QMessageBox

class UserManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("User Manager System")
        self.setGeometry(430,200,600,400)

        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Username", "Password", "Email"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        self.setCentralWidget(self.table)

        self.table.cellClicked.connect(self.cell_selected)

    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="1234",
                database="users_db"
            )
            if connection.is_connected():
                return connection
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error connecting to database: {e}")
            return None

    def cell_selected(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserManager()
    window.show()
    app.exec()