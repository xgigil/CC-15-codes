from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from cafe_ui import Ui_MainWindow
from datetime import datetime
from random import randint

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.drinks = {
            self.icedCappuccinoBox: (self.drinksSpinBox_icedCap, 90),
            self.americanCoffeeBox: (self.drinksSpinBox_american, 85),
            self.africanCoffeeBox: (self.drinksSpinBox_african, 80),
            self.valesBox: (self.drinksSpinBox_vales, 95),
            self.CappuccinoBox: (self.drinksSpinBox_cappuccino, 100),
            self.icedlatteBox: (self.drinksSpinBox_icedlatte, 100),
            self.espressoBox: (self.drinksSpinBox_espresso, 120),
            self.latteBox: (self.drinksSpinBox_latte, 110)
        }

        self.cakes = {
            self.queenchocoBox: (self.chocoSpinBox_queens, 350),
            self.carltonBox: (self.chocoSpinBox_carlton, 360),
            self.kilburnBox: (self.chocoSpinBox_kilburn, 345),
            self.lagosBox: (self.chocoSpinBox_lagos, 355),
            self.bostonBox: (self.chocoSpinBox_boston, 350),
            self.blackforestBox: (self.chocoSpinBox_blackforest, 370),
            self.rvBox: (self.chocoSpinBox_redvelvet, 375),
            self.coffeecakeBox: (self.chocoSpinBox_coffeecake, 365)
        }

        self.totalButton.clicked.connect(self.calculate_total)
        self.receiptButton.clicked.connect(self.generate_receipt)
        self.resetButton.clicked.connect(self.reset_fields)
        self.exitButton.clicked.connect(self.close_app)

    def calculate_total(self):
        total_drinks = 0
        total_cakes = 0

        for checkbox, (spinbox, price) in self.drinks.items():
            if checkbox.isChecked():
                qty = spinbox.value()
                total_drinks += qty * price

        for checkbox, (spinbox, price) in self.cakes.items():
            if checkbox.isChecked():
                qty = spinbox.value()
                total_cakes += qty * price

        service_charge = 25.00
        subtotal = total_drinks + total_cakes + service_charge
        tax = subtotal * 0.12
        total = subtotal + tax

        self.lineEdit_drinksTotal.setText(f"₱{total_drinks:.2f}")
        self.lineEdit_cakesTotal.setText(f"₱{total_cakes:.2f}")
        self.lineEdit_service.setText(f"₱{service_charge:.2f}")
        self.lineEdit_tax.setText(f"₱{tax:.2f}")
        self.lineEdit_subtotal.setText(f"₱{subtotal:.2f}")
        self.lineEdit_total.setText(f"₱{total:.2f}")

    def generate_receipt(self):
        reply = QMessageBox.question(
            self,
            'Create Receipt',
            'Are you sure you want to create receipt?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            receipt_lines = []
            total_drinks = 0
            total_cakes = 0

            receipt_id = randint(10000, 99999)
            now = datetime.now()

            receipt_lines.append("=" * 40)
            receipt_lines.append("             Just Do Coffee")
            receipt_lines.append(f"           Receipt No: #{receipt_id}")
            receipt_lines.append("=" * 40)
            receipt_lines.append(now.strftime("Date: %d %B %Y     Time: %I:%M %p"))
            receipt_lines.append("-" * 40)

            for checkbox, (spinbox, price) in self.cakes.items():
                if checkbox.isChecked():
                    qty = spinbox.value()
                    if qty > 0:
                        cost = qty * price
                        receipt_lines.append(f"{checkbox.text():<25} {qty:>2} x ₱{price:<3} = ₱{cost:>5f}")
                        total_cakes += cost

            for checkbox, (spinbox, price) in self.drinks.items():
                if checkbox.isChecked():
                    qty = spinbox.value()
                    if qty > 0:
                        cost = qty * price
                        receipt_lines.append(f"{checkbox.text():<25} {qty:>2} x ₱{price:<3} = ₱{cost:>5f}")
                        total_drinks += cost

            receipt_lines.append("-" * 40)
            service_charge = 25.00
            subtotal = total_drinks + total_cakes + service_charge
            tax = subtotal * 0.12
            total = subtotal + tax

            receipt_lines.append(f"{'Service Charge':<28} ₱{service_charge:>5f}")
            receipt_lines.append(f"{'Tax (12%)':<28} ₱{tax:>5f}")
            receipt_lines.append(f"{'Subtotal':<28} ₱{subtotal:>5f}")
            receipt_lines.append(f"{'TOTAL':<28} ₱{total:>5f}")
            receipt_lines.append("=" * 40)

            receipt_lines.append("\nThank you for visiting Just Do Coffee!")
            receipt_lines.append("Have a great day! ☕")

            receipt = "\n".join(receipt_lines)
            self.receiptBrowser.setPlainText(receipt)

    def reset_fields(self):
        reply = QMessageBox.question(
            self,
            'Reset Fields',
            'Are you sure you want to reset fields?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            for checkbox, (spinbox, _) in self.drinks.items():
                checkbox.setChecked(False)
                spinbox.setValue(0)

            for checkbox, (spinbox, _) in self.cakes.items():
                checkbox.setChecked(False)
                spinbox.setValue(0)

            self.lineEdit_drinksTotal.clear()
            self.lineEdit_cakesTotal.clear()
            self.lineEdit_service.clear()
            self.lineEdit_tax.clear()
            self.lineEdit_subtotal.clear()
            self.lineEdit_total.clear()
            self.receiptBrowser.clear()

    def close_app(self):
        reply = QMessageBox.question(
            self,
            'Exit Application',
            'Are you sure you want to exit?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.close()

app = QApplication([])
window = MyApp()
window.show()
app.exec()