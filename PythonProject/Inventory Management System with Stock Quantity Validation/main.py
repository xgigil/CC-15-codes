import sys
import mysql.connector
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QPushButton, QLabel, \
    QWidget, QFormLayout, QVBoxLayout
from mysql.connector import Error

class DatabaseApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Warehouse Inventory System")
        self.setGeometry(500,200,400,150)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.productName_input = QLineEdit(self)
        self.productQuantity_input = QLineEdit(self)
        self.productPrice_input = QLineEdit(self)

        self.addProduct_button = QPushButton("Add Product", self)
        self.addProduct_button.clicked.connect(self.add_product)

        form_layout = QFormLayout()
        form_layout.addRow("Product Name:", self.productName_input)
        form_layout.addRow("Quantity:", self.productQuantity_input)
        form_layout.addRow("Price:", self.productPrice_input)

        self.layout = QVBoxLayout()
        self.layout.addLayout(form_layout)
        self.layout.addWidget(self.addProduct_button)

        central_widget.setLayout(self.layout)

    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="1234",
                database="inventorydb"
            )
            if connection.is_connected():
                return connection
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error connecting to database: {e}")
            return None

    def add_product(self):
        try:
            connection = self.connect_to_database()
            if connection:
                cursor = connection.cursor()

                if not self.productName_input.text() or not self.productQuantity_input.text() or not self.productPrice_input.text():
                    QMessageBox.warning(self, "Input Error", "All fields must be filled.")
                    return

                if not self.productQuantity_input.text().isdigit() >= 0:
                    QMessageBox.warning(self, "Quantity Error", "Quantity must be a valid whole number")
                    return

                try:
                    float(self.productPrice_input.text())
                except ValueError:
                    QMessageBox.warning(self, "Price Error", "Price must be a valid positive number")
                    return

                check_query = "SELECT * FROM inventory WHERE product_name = %s"
                check_value = (self.productName_input.text(),)
                cursor.execute(check_query, check_value)
                user = cursor.fetchone()

                if user:
                    QMessageBox.warning(self, "Product Error", "Product already exists.")
                    cursor.close()
                    connection.close()
                    return

                query = "INSERT INTO inventory (product_name,quantity,price) VALUES (%s,%s,%s)"
                values = (self.productName_input.text(),self.productQuantity_input.text(),self.productPrice_input.text())
                cursor.execute(query,values)
                connection.commit()

                QMessageBox.information(self, "Success", "Product Added!")

                cursor.close()
                connection.close()
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error connecting to database: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatabaseApp()
    window.show()
    app.exec()