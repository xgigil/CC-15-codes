from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

app = QApplication([])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My first PyQt6 App")
        self.setGeometry(100,100,400,300) #set window position

        self.create_widgets()

    def create_widgets(self):
        button = QPushButton("Click Me", self)
        button.setGeometry(150,150,100,50) #set button position
        button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        print("Button clicked!")

window = MainWindow()
window.show()
app.exec()