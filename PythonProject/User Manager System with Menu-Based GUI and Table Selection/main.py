import sys
import mysql.connector
from mysql.connector import Error
from PyQt6.QtWidgets import QApplication, QMenuBar, QMainWindow, QLineEdit, QPushButton, \
    QLabel, QTableWidget, QWidget, QMessageBox, QTableWidgetItem, QDialog, QVBoxLayout, QFormLayout, \
    QHBoxLayout
from PyQt6.QtGui import QAction


class AddUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New User")

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.email_input = QLineEdit()

        self.addUser_button = QPushButton("Add", self)
        self.addUser_button.clicked.connect(self.add_user)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.cancel_add)

        form_layout = QFormLayout()
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("Email:", self.email_input)

        self.HBox_layout = QHBoxLayout()
        self.HBox_layout.addLayout(self.addUser_button)
        self.HBox_layout.addLayout(self.cancel_button)

        self.layout = QVBoxLayout()
        self.layout.addLayout(form_layout)
        self.layout.addWidget(self.HBox_layout)

class UserManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("User Manager System")
        self.setGeometry(430, 200, 600, 400)

        self.table = QTableWidget(self)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.cellClicked.connect(self.cell_selected)
        self.setCentralWidget(self.table)

        self.generate_menu()
        self.load_data()

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

    def generate_menu(self):
        menubar = self.menuBar()

        user_menu = menubar.addMenu("User")
        add_user_action = QAction("Add New User", self)
        add_user_action.triggered.connect(self.add_new_user)
        user_menu.addAction(add_user_action)

        delete_user_action = QAction("Delete Selected User", self)
        delete_user_action.triggered.connect(self.delete_selected_user)
        user_menu.addAction(delete_user_action)

        refresh_action = QAction("Refresh Table", self)
        refresh_action.triggered.connect(self.load_data)
        user_menu.addAction(refresh_action)

        actions_menu = menubar.addMenu("Actions")
        dummy_action = QAction("Add Dummy User", self)
        dummy_action.triggered.connect(self.add_dummy_user)
        actions_menu.addAction(dummy_action)

        clear_selection_action = QAction("Clear Selection", self)
        clear_selection_action.triggered.connect(self.clear_selection)
        actions_menu.addAction(clear_selection_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        actions_menu.addAction(exit_action)

    def load_data(self):

        try:
            connection = self.connect_to_database()

            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM accounts")

                rows = cursor.fetchall()
                self.table.setRowCount(len(rows))
                self.table.setColumnCount(4)
                self.table.setHorizontalHeaderLabels(["ID", "Username", "Password", "Email"])

                for row_index, row in enumerate(rows):
                    for col_index, item in enumerate(row):
                        self.table.setItem(row_index, col_index, QTableWidgetItem(str(item)))

                connection.close()
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error connecting to database: {e}")

    def cell_selected(self, row, column):
        item = self.table.item(row, 0)
        if item:
            self.selected_user_id = int(item.text())

    def add_new_user(self):
        dialog = AddUserDialog()
        dialog.addUser_button.clicked.connect(lambda: self.submit_new_user(dialog))
        dialog.exec()

    def submit_new_user(self, dialog):
        username = dialog.username_input.text()
        password = dialog.password_input.text()
        email = dialog.email_input.text()

        if not username or not password or not email:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        connection = self.connect_to_database()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)",
                               (username, password, email))
                connection.commit()
                QMessageBox.information(self, "Success", "User added successfully.")
                dialog.close()
                self.load_data()
            except Error as e:
                QMessageBox.critical(self, "Error", f"Failed to add user: {e}")
            finally:
                connection.close()

    def delete_selected_user(self):
        if self.selected_user_id is None:
            QMessageBox.warning(self, "Selection Error", "No user selected.")
            return

        confirmation = QMessageBox.question(self, "Confirm Delete",
                                            f"Are you sure you want to delete user ID {self.selected_user_id}?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation == QMessageBox.StandardButton.Yes:
            connection = self.connect_to_database()
            if connection:
                cursor = connection.cursor()
                try:
                    cursor.execute("DELETE FROM accounts WHERE id = %s", (self.selected_user_id,))
                    connection.commit()
                    QMessageBox.information(self, "Deleted", "User deleted successfully.")
                    self.selected_user_id = None
                    self.load_data()
                except Error as e:
                    QMessageBox.critical(self, "Error", f"Failed to delete user: {e}")
                finally:
                    connection.close()

    def add_dummy_user(self):
        connection = self.connect_to_database()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)",
                               ("dummy_user", "dummy123", "dummy@example.com"))
                connection.commit()
                QMessageBox.information(self, "Success", "Dummy user added.")
                self.load_data()
            except Error as e:
                QMessageBox.critical(self, "Error", f"Failed to add dummy user: {e}")
            finally:
                connection.close()

    def clear_selection(self):
        self.table.clearSelection()
        self.selected_user_id = None

    def cancel_add(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserManager()
    window.show()
    app.exec()
