import mysql.connector
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
                password="Looking@11072004",
                database="users"
            )
            if connection.is_connected():
                return connection
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error connecting to database: {e}")
            return None

    def login_account(self):
        try:
            connection = self.connect_to_database()
            if connection:
                cursor = connection.cursor()
                query = "SELECT * FROM users WHERE username = %s AND password = %s"
                username = self.username_input.text()
                password = self.password_input.text()
                cursor.execute(query, (username, password))
                user = cursor.fetchone()

                if user:
                    QMessageBox.information(self, "Login Successful", f"Welcome {username}!")
                else:
                    QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

                cursor.close()
                connection.close()
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error connecting to database: {e}")

app = QApplication([])
window = MyApp()
window.show()
app.exec()
