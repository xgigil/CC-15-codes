from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow


class CafeManagementSystem(QMainWindow):
    def __int__(self):
        super().__init__()
        uic.loadUi('cafe.ui', self)

app = QApplication([])
window = uic.loadUi("cafe.ui")
window.show()
app.exec()