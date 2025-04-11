#from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

#app = QApplication([])
#window = uic.loadUi("cafe.ui")
#window.show()
#app.exec()

import cafe_ui

if hasattr(cafe_ui, 'Ui_MainWindow'):
        ui = cafe_ui.Ui_MainWindow()
else:
        ui = cafe_ui.UiForm()



app = QApplication([])
window = QMainWindow()
ui.setupUi(window)
window.show()
app.exec()
