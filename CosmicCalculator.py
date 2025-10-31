import sys
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIcon, QFont, QColor, QPainter, QBrush
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QGridLayout, QHBoxLayout, QLabel, QGraphicsDropShadowEffect
)


class CosmicCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cosmic Calculator")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(380, 540)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowIcon(QIcon("icon.ico"))
        self.offset = None

        # Outer transparent layer
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        # Inner container with rounded corners (no double round)
        self.container = QWidget()
        self.container.setObjectName("container")
        self.container.setStyleSheet("""
            QWidget#container {
                background: rgba(30, 0, 60, 180);
                border-radius: 20px;
                backdrop-filter: blur(25px);
            }
        """)
        outer_layout.addWidget(self.container)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Title Bar ---
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("""
            background-color: rgba(25, 0, 45, 240);
            border-top-left-radius: 20px;
            border-top-right-radius: 20px;
        """)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 15, 0)

        self.title_label = QLabel("⚡ Cosmic Calculator")
        self.title_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()

        self.min_btn = self.create_window_btn("—")
        self.max_btn = self.create_window_btn("□")
        self.close_btn = self.create_window_btn("✕", danger=True)
        self.min_btn.clicked.connect(self.showMinimized)
        self.max_btn.clicked.connect(self.toggleMax)
        self.close_btn.clicked.connect(self.close)

        title_layout.addWidget(self.min_btn)
        title_layout.addWidget(self.max_btn)
        title_layout.addWidget(self.close_btn)

        layout.addWidget(title_bar)

        # --- Display ---
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFont(QFont("Consolas", 20))
        self.display.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.12);
                border: none;
                border-bottom: 2px solid rgba(255, 255, 255, 0.25);
                color: white;
                padding: 15px;
                margin: 15px;
                border-radius: 10px;
            }
        """)
        layout.addWidget(self.display)

        # --- Buttons Grid ---
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(20, 0, 20, 20)

        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('⌫', 3, 2), ('+', 3, 3),
            ('C', 4, 0), ('=', 4, 1, 1, 3)
        ]

        for text, row, col, *span in buttons:
            btn = QPushButton(text)
            btn.setFont(QFont("Segoe UI", 14))
            btn.setStyleSheet(self.button_style("=" if text == "=" else text))
            btn.clicked.connect(self.on_button_click)
            grid_layout.addWidget(btn, row, col, *span if span else (1, 1))

        layout.addWidget(grid_widget)

        # Shadow glow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(160, 0, 255, 120))
        shadow.setOffset(0, 0)
        self.container.setGraphicsEffect(shadow)

    # --- Button Styling ---
    def button_style(self, text):
        if text == "=":
            return """
                QPushButton {
                    background-color: qlineargradient(
                        spread:pad, x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(180, 0, 255, 230),
                        stop:1 rgba(255, 0, 200, 230)
                    );
                    color: white; border-radius: 10px;
                    font-weight: bold; padding: 10px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 0, 200, 255);
                }
            """
        return """
            QPushButton {
                background-color: rgba(90, 0, 140, 130);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgba(160, 0, 255, 200);
                box-shadow: 0px 0px 10px rgba(255, 100, 255, 100);
            }
        """

    def create_window_btn(self, text, danger=False):
        btn = QPushButton(text)
        btn.setFixedSize(30, 30)
        btn.setStyleSheet(f"""
            QPushButton {{
                color: white; border: none;
                background: transparent; border-radius: 8px;
            }}
            QPushButton:hover {{
                background: rgba({'255, 0, 70, 80' if danger else '255, 255, 255, 50'});
            }}
        """)
        return btn

    # --- Button Logic ---
    def on_button_click(self):
        text = self.sender().text()
        if text == "C":
            self.display.clear()
        elif text == "=":
            try:
                expression = self.display.text().replace('×', '*').replace('÷', '/')
                result = str(eval(expression))
                self.display.setText(result)
            except:
                self.display.setText("Error")
        elif text == "⌫":
            self.display.backspace()
        else:
            self.display.setText(self.display.text() + text)

    # --- Keyboard Input ---
    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()
        if key in range(Qt.Key.Key_0, Qt.Key.Key_9 + 1) or text in "+-*/.":
            self.display.setText(self.display.text() + text)
        elif key == Qt.Key.Key_Backspace:
            self.display.backspace()
        elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            try:
                result = str(eval(self.display.text()))
                self.display.setText(result)
            except:
                self.display.setText("Error")
        elif key == Qt.Key.Key_Escape:
            self.close()

    # --- Window Controls ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.offset and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.offset = None

    def toggleMax(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    calc = CosmicCalculator()
    calc.show()
    sys.exit(app.exec())
