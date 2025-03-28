from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Message Box Example")
        self.setGeometry(100,100,300,200)

        self.button = QPushButton("Show Message", self)
        self.button.setGeometry(80,80,140,40)
        self.button.clicked.connect(self.show_message)

    def show_message(self):
        QMessageBox.information(self, "Message", "Hello from PyQt6!")

app = QApplication([])
window = MainWindow()
window.show()
app.exec()