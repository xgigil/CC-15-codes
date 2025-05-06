import sys
import mysql.connector
from mysql.connector import Error
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QApplication, QGridLayout, QLabel, QLineEdit, QMessageBox

class Window(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        self.setWindowTitle("CodersLegacy")
        self.setLayout(layout)

        self.setStyleSheet(open("style.css", "r").read())

        # Title Label
        title = QLabel("Login Form with PyQt6")
        title.setProperty("class", "heading")
        layout.addWidget(title, 0, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)

        # Username Label and Input
        user = QLabel("Username:")
        user.setProperty("class", "normal")
        layout.addWidget(user, 1, 0)
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input, 1, 1, 1, 2)

        # Password Label and Input
        pwd = QLabel("Password")
        pwd.setProperty("class", "normal")
        layout.addWidget(pwd, 2, 0)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input, 2, 1, 1, 2)

        # Register and Login Buttons
        button1 = QPushButton("Register")
        layout.addWidget(button1, 4, 1)

        loginButton = QPushButton("Login")
        loginButton.clicked.connect(self.login)
        layout.addWidget(loginButton, 4, 2)

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

    def login(self):
        try:
            connection = self.connect_to_database()
            if connection:
                cursor = connection.cursor()
                query = "SELECT * FROM accounts WHERE username = %s AND password = %s"
                username = self.username_input.text()
                password = self.password_input.text()
                cursor.execute(query, (username, password))
                user = cursor.fetchone()

                if user:
                    QMessageBox.information(self, "Login Successful", f"Welcome {username}!")
                elif not self.username_input.text() or not self.password_input.text():
                    QMessageBox.warning(self, "Input Error", "All fields must be filled.")
                else:
                    QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

                cursor.close()
                connection.close()
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error connecting to database: {e}")


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())