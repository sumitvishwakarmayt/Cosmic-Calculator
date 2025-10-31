from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout
import sys

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Brainrot Calculator 💀")
        self.setGeometry(200, 200, 300, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.display = QLineEdit()
        layout.addWidget(self.display)

        grid = QGridLayout()
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+']
        ]

        for row, row_values in enumerate(buttons):
            for col, btn_text in enumerate(row_values):
                btn = QPushButton(btn_text)
                btn.clicked.connect(lambda _, text=btn_text: self.on_click(text))
                grid.addWidget(btn, row, col)

        layout.addLayout(grid)
        self.setLayout(layout)

    def on_click(self, text):
        if text == '=':
            try:
                result = str(eval(self.display.text()))
                self.display.setText(result)
            except:
                self.display.setText("Error💀")
        else:
            self.display.setText(self.display.text() + text)


app = QApplication(sys.argv)
window = Calculator()
window.show()
sys.exit(app.exec())
