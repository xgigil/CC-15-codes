from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel

class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Second Window")
        self.setGeometry(150,150,300,150)

        layout = QVBoxLayout()
        label = QLabel("This is the second window")
        layout.addWidget(label)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 300, 200)

        self.button = QPushButton("Open Second Window", self)
        self.button.setGeometry(60,80,180,40)
        self.button.clicked.connect(self.open_second_window)

    def open_second_window(self):
        self.second_window = SecondWindow()
        self.second_window.show()

app = QApplication([])
window = MainWindow()
window.show()
app.exec()