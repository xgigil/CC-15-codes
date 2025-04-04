from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QLabel, QWidget, \
    QLineEdit, QComboBox


class ContactManager:
    def __init__(self):
        self.contacts = {}

    def add_contact(self, name, phone, email, category):
        if not all([name.strip(), phone.strip(), email.strip(), category.strip()]):
            return "Error: All fields need to be inputted."
        if name in self.contacts:
            return "Contact already exists."
        self.contacts[name] = (phone, email, category)
        return f"Contact Added: {name} (Phone: {phone}, Email: {email}, Category: {category})"

    def display_contacts(self):
        if not self.contacts:
            return "No contacts to be displayed."
        contact_list = "Contacts List:\n"
        contact_list += "\n".join([f"{i}. {name} - Phone: {phone}, Email: {email}, Category: {category}"
                                   for i, (name, (phone, email, category)) in enumerate(self.contacts.items(), 1)])
        return contact_list

    def search_contact(self, name):
        if name in self.contacts:
            phone, email, category = self.contacts[name]
            return f"Contact Found: {name}, - Phone: {phone}, Email: {email}, Category: {category}"
        else:
            return "Contact not found."

    def delete_contact(self, name):
        if name in self.contacts:
            del self.contacts[name]
            return f"{name} has been removed from contacts"
        else:
            return "Contact not found."

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.manager = ContactManager()

        self.setWindowTitle("Contact Management App")
        self.setGeometry(100, 100, 300, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.label = QLabel("Enter Name:")
        self.layout.addWidget(self.label)
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_input)

        self.label = QLabel("Enter Phone:")
        self.layout.addWidget(self.label)
        self.phone_input = QLineEdit()
        self.layout.addWidget(self.phone_input)

        self.label = QLabel("Enter Email:")
        self.layout.addWidget(self.label)
        self.email_input = QLineEdit()
        self.layout.addWidget(self.email_input)

        self.label = QLabel("Select Category:")
        self.layout.addWidget(self.label)
        self.category_select = QComboBox()
        self.category_select.addItems(["Family", "Friends", "Work", "Others"])
        self.layout.addWidget(self.category_select)

        self.add_button = QPushButton("Add Contact", self)
        self.add_button.clicked.connect(self.add_contact)
        self.layout.addWidget(self.add_button)

        self.search_button = QPushButton("Search Contact", self)
        self.search_button.clicked.connect(self.search_contact)
        self.layout.addWidget(self.search_button)

        self.display_button = QPushButton("Display Contact", self)
        self.display_button.clicked.connect(self.display_contacts)
        self.layout.addWidget(self.display_button)

        self.delete_button = QPushButton("Delete Contact", self)
        self.delete_button.clicked.connect(self.delete_contact)
        self.layout.addWidget(self.delete_button)

        self.central_widget.setLayout(self.layout)

    def add_contact(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        category = self.category_select.currentText()
        message = self.manager.add_contact(name, phone, email, category)
        if "Error" in message or "already exists" in message:
            QMessageBox.critical(self, "Error", message)
        else:
            QMessageBox.information(self, "Info", message)

    def search_contact(self):
        name = self.name_input.text()
        message = self.manager.search_contact(name)
        if "not found" in message:
            QMessageBox.critical(self, "Error", message)
        else:
            QMessageBox.information(self, "Info", message)

    def display_contacts(self):
        message = self.manager.display_contacts()
        if "No contacts to be displayed" in message:
            QMessageBox.critical(self, "Error", message)
        else:
            QMessageBox.information(self, "Info", message)

    def delete_contact(self):
        name = self.name_input.text()
        message = self.manager.delete_contact(name)
        if "not found" in message:
            QMessageBox.critical(self, "Error", message)
        else:
            QMessageBox.information(self, "Info", message)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()