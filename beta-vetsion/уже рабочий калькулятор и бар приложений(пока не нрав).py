import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QLCDNumber, QDialog, QGridLayout
from PyQt5.QtCore import QTimer, Qt

class CalculatorWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Калькулятор")
        layout = QVBoxLayout()

        self.result_display = QLineEdit()
        self.result_display.setReadOnly(True)  # Set display to read-only
        layout.addWidget(self.result_display)

        buttons_layout = QGridLayout()

        buttons = [
            ("7", (0, 0)),
            ("8", (0, 1)),
            ("9", (0, 2)),
            ("/", (0, 3)),
            ("4", (1, 0)),
            ("5", (1, 1)),
            ("6", (1, 2)),
            ("*", (1, 3)),
            ("1", (2, 0)),
            ("2", (2, 1)),
            ("3", (2, 2)),
            ("-", (2, 3)),
            ("0", (3, 0)),
            (".", (3, 1)),
            ("=", (3, 2)),
            ("+", (3, 3)),
            ("C", (4, 0, 1, 4)),
        ]

        for button_text, pos in buttons:
            button = QPushButton(button_text)
            if len(pos) == 2:
                buttons_layout.addWidget(button, *pos)
            else:
                buttons_layout.addWidget(button, *pos, alignment=Qt.AlignCenter)
            if button_text != '=' and button_text != 'C':
                button.clicked.connect(lambda _, text=button_text: self.update_display(text))
            elif button_text == '=':
                button.clicked.connect(self.handle_equal)
            else:
                button.clicked.connect(self.handle_clear)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

        self.calculation_to_eval = ""

    def update_display(self, value):
        self.calculation_to_eval += value
        self.result_display.setText(self.calculation_to_eval)

    def calculate(self):
        try:
            result = eval(self.calculation_to_eval)
            self.result_display.setText(str(result))
            self.calculation_to_eval = ""
        except Exception as e:
            self.result_display.setText("Ошибка")
            self.calculation_to_eval = ""

    def clear_display(self):
        self.result_display.clear()
        self.calculation_to_eval = ""

    def handle_equal(self):
        self.calculate()

    def handle_clear(self):
        self.clear_display()

class TimerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Таймер")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.timer_lcd = QLCDNumber()
        self.timer_lcd.setDigitCount(8)
        layout.addWidget(self.timer_lcd)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.start_button = QPushButton("Старт")
        self.start_button.clicked.connect(self.start_timer)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def start_timer(self):
        self.timer.start(1000)  # Запускаем таймер, обновление каждую секунду

    def update_timer(self):
        time = self.timer_lcd.value()
        time += 1
        self.timer_lcd.display(time)

class AppSelectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор приложения")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        calculator_button = QPushButton("Калькулятор")
        calculator_button.clicked.connect(self.open_calculator)
        layout.addWidget(calculator_button)

        timer_button = QPushButton("Таймер")
        timer_button.clicked.connect(self.open_timer)
        layout.addWidget(timer_button)

        self.setLayout(layout)

    def open_calculator(self):
        self.calculator_window = CalculatorWindow()
        self.calculator_window.show()

    def open_timer(self):
        self.timer_window = TimerWindow()
        self.timer_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    selection_window = AppSelectionWindow()
    selection_window.show()
    sys.exit(app.exec_())
