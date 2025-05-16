import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox, QComboBox, QInputDialog
)
from PyQt6.QtCore import Qt
import mysql.connector
from mysql.connector import Error
import bcrypt
from config import verify_role_password

# --- Welcome Window ---
class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Organization Profiling System")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        title = QLabel("Welcome to the Organization Profiling System")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        button_layout.addWidget(login_button)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.open_register_window)
        button_layout.addWidget(register_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

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

    def login(self):
        connection = self.connect_to_database()
        if connection:
            try:
                cursor = connection.cursor()
                username = self.username_input.text()
                password = self.password_input.text()

                query = "SELECT password, role FROM accounts WHERE username=%s"
                cursor.execute(query, (username,))
                result = cursor.fetchone()

                if result and bcrypt.checkpw(password.encode(), result[0].encode()):
                    role = result[1]
                    try:
                        if role == "Admin":
                            self.dashboard = AdminDashboard(username)
                        elif role == "Executive":
                            self.dashboard = ExecutiveDashboard(username)
                        elif role == "Member":
                            self.dashboard = MemberDashboard(username)
                        else:
                            raise ValueError(f"Unknown role: {role}")
                        
                        self.dashboard.show()
                        self.hide()
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Error creating window: {str(e)}")
                else:
                    QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
            finally:
                cursor.close()
            connection.close()

    def open_register_window(self):
        self.register_window = RegisterWindow(self)
        self.register_window.show()
        self.hide()

# --- Register Window ---
class RegisterWindow(QWidget):
    def __init__(self, welcome_window):
        super().__init__()
        self.welcome_window = welcome_window
        self.setWindowTitle("Register")
        self.setGeometry(100, 100, 400, 400)

        layout = QGridLayout()

        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("First Name (All Caps)")
        layout.addWidget(self.first_name, 0, 0, 1, 2)

        self.middle_name = QLineEdit()
        self.middle_name.setPlaceholderText("Middle Name (All Caps)")
        layout.addWidget(self.middle_name, 1, 0, 1, 2)

        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("Last Name (All Caps)")
        layout.addWidget(self.last_name, 2, 0, 1, 2)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        layout.addWidget(self.username, 3, 0, 1, 2)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password, 4, 0, 1, 2)

        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Confirm Password")
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_password, 5, 0, 1, 2)

        self.role_box = QComboBox()
        self.role_box.addItems(["Member", "Executive"])
        layout.addWidget(self.role_box, 6, 0, 1, 2)

        register_btn = QPushButton("Register")
        register_btn.clicked.connect(self.register_account)
        layout.addWidget(register_btn, 7, 0)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn, 7, 1)

        self.setLayout(layout)

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

    def register_account(self):
        fn = self.first_name.text()
        mn = self.middle_name.text()
        ln = self.last_name.text()
        un = self.username.text()
        pw = self.password.text()
        cpw = self.confirm_password.text()
        role = self.role_box.currentText()

        # Validate caps
        if not (fn.isupper() and mn.isupper() and ln.isupper()):
            QMessageBox.warning(self, "Invalid Input", "First name, middle name, and last name must be in ALL CAPS!")
            return

        if pw != cpw:
            QMessageBox.warning(self, "Password Mismatch", "Passwords do not match.")
            return

        # Role password verification
        input_password, ok = QInputDialog.getText(self, "Role Password",
                                                f"Enter {role} role password:",
                                                QLineEdit.EchoMode.Password)
        if not ok:
            return

        # Verify role-specific password using the new verification function
        if not verify_role_password(role, input_password):
            QMessageBox.warning(self, "Incorrect Password", "Incorrect role-specific password.")
            return

        # Hash the user's password
        hashed_password = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())

        connection = self.connect_to_database()
        if connection:
            try:
                cursor = connection.cursor()
                query = """INSERT INTO accounts 
                        (first_name, middle_name, last_name, username, password, role) 
                        VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (fn, mn, ln, un, hashed_password, role))
                connection.commit()
                QMessageBox.information(self, "Success", "Registration complete!")
                self.go_back()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Error", f"Registration error: {str(e)}")
            finally:
                cursor.close()
                connection.close()

    def go_back(self):
        self.welcome_window.show()
        self.close()

class AdminDashboard(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Admin Dashboard")
        layout = QVBoxLayout()

        # Welcome message
        welcome_label = QLabel(f"Welcome Administrator {self.username}")
        layout.addWidget(welcome_label)

        # Admin Functions
        functions_layout = QVBoxLayout()
        
        # User Management
        manage_users_btn = QPushButton("Manage All Users")
        manage_users_btn.clicked.connect(self.manage_users)
        functions_layout.addWidget(manage_users_btn)
        
        # View All Profiles
        view_profiles_btn = QPushButton("View All Profiles")
        view_profiles_btn.clicked.connect(self.view_all_profiles)
        functions_layout.addWidget(view_profiles_btn)
        
        # System Settings
        system_settings_btn = QPushButton("System Settings")
        system_settings_btn.clicked.connect(self.system_settings)
        functions_layout.addWidget(system_settings_btn)

        layout.addLayout(functions_layout)
        self.setLayout(layout)

    def manage_users(self):
        pass  # Implement user management functionality

    def view_all_profiles(self):
        pass  # Implement profile viewing functionality

    def system_settings(self):
        pass  # Implement settings functionality


class ExecutiveDashboard(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Executive Dashboard")
        layout = QVBoxLayout()

        welcome_label = QLabel(f"Welcome Executive {self.username}")
        layout.addWidget(welcome_label)

        # Executive Functions
        functions_layout = QVBoxLayout()
        
        # Pending Registrations
        pending_reg_btn = QPushButton("Pending Registrations")
        pending_reg_btn.clicked.connect(self.view_pending_registrations)
        functions_layout.addWidget(pending_reg_btn)
        
        # Member Management
        manage_members_btn = QPushButton("Manage Members")
        manage_members_btn.clicked.connect(self.manage_members)
        functions_layout.addWidget(manage_members_btn)
        
        # Deletion Requests
        deletion_requests_btn = QPushButton("Deletion Requests")
        deletion_requests_btn.clicked.connect(self.view_deletion_requests)
        functions_layout.addWidget(deletion_requests_btn)

        layout.addLayout(functions_layout)
        self.setLayout(layout)

    def view_pending_registrations(self):
        pass  # Implement registration approval functionality

    def manage_members(self):
        pass  # Implement member management functionality

    def view_deletion_requests(self):
        pass  # Implement deletion request handling


class MemberDashboard(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Member Dashboard")
        layout = QVBoxLayout()

        welcome_label = QLabel(f"Welcome Member {self.username}")
        layout.addWidget(welcome_label)

        # Member Functions
        functions_layout = QVBoxLayout()
        
        # View/Edit Profile
        profile_btn = QPushButton("My Profile")
        profile_btn.clicked.connect(self.view_profile)
        functions_layout.addWidget(profile_btn)
        
        # View Member Directory
        directory_btn = QPushButton("Member Directory")
        directory_btn.clicked.connect(self.view_directory)
        functions_layout.addWidget(directory_btn)
        
        # Request Account Deletion
        delete_btn = QPushButton("Request Account Deletion")
        delete_btn.clicked.connect(self.request_deletion)
        functions_layout.addWidget(delete_btn)

        layout.addLayout(functions_layout)
        self.setLayout(layout)

    def view_profile(self):
        pass  # Implement profile viewing/editing functionality

    def view_directory(self):
        pass  # Implement directory viewing functionality

    def request_deletion(self):
        pass

# --- Main ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WelcomeWindow()
    window.show()
    sys.exit(app.exec())