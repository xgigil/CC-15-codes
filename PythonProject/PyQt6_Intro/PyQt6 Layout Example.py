from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 Layout Example")
        self.setGeometry(100,100,400,300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.label = QLabel("Hello, PyQt6!")
        self.layout.addWidget(self.label)

        self.button = QPushButton("Change Text")
        self.button.clicked.connect(self.change_text)
        self.layout.addWidget(self.button)

        self.central_widget.setLayout(self.layout)

    def change_text(self):
        self.label.setText("Text Changed!")

app = QApplication([])
window = MainWindow()
window.show()
app.exec()