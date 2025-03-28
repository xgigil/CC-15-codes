from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 Line Edit")
        self.setGeometry(100,100,400,300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.label = QLabel("Enter your name:")
        self.layout.addWidget(self.label)

        self.text_input = QLineEdit()
        self.layout.addWidget(self.text_input)

        self.button = QPushButton("Submit")
        self.button.clicked.connect(self.display_text)
        self.layout.addWidget(self.button)

        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)

        self.central_widget.setLayout(self.layout)

    def display_text(self):
        user_input = self.text_input.text()
        self.result_label.setText(f"Hello, {user_input}!")

app = QApplication([])
window = MainWindow()
window.show()
app.exec()