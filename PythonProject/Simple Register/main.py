import sys
import mysql.connector
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QPushButton, QLabel, QVBoxLayout, \
    QWidget
from mysql.connector import Error

class DatabaseApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple Register")
        self.setGeometry(100,100,400,400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter Username")

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter Password")

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Enter Email")

        self.register_button = QPushButton("Register", self)

        self.register_button.clicked.connect(self.register_account)

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(self.register_button)

        central_widget.setLayout(self.layout)

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

    def register_account(self):
        try:
            connection = self.connect_to_database()
            if connection:
                cursor = connection.cursor()

                c_query = "SELECT * FROM accounts WHERE username = %s"
                c_values = (self.username_input.text())
                cursor.execute(c_query, c_values)
                user = cursor.fetchone()

                if user:
                    QMessageBox.warning(self, "Username Error", "Username already in use.")
                    cursor.close()
                    connection.close()
                    return

                query = "INSERT INTO accounts (username,password,email) VALUES (%s,%s,%s)"
                values = (self.username_input.text(),self.password_input.text(),self.email_input.text())
                cursor.execute(query,values)
                connection.commit()

                if not self.username_input.text() or self.password_input.text() or self.email_input.text():
                    QMessageBox.warning(self, "Input Error", "All fields must be filled.")
                else:
                    QMessageBox.information(self, "Success", "Account Registered!")

                cursor.close()
                connection.close()
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error connecting to database: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatabaseApp()
    window.show()
    app.exec()