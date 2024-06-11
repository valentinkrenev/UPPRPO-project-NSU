import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QLCDNumber, QDialog
from PyQt5.QtCore import QTimer


from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QGridLayout, QDialog
from PyQt5.QtCore import Qt

class CalculatorWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Калькулятор")
        layout = QVBoxLayout()

        self.result_display = QLineEdit()
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
            button.clicked.connect(lambda _, text=button_text: self.update_display(text))

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

        # Добавленные обработчики

    def handle_equal(self):
        self.calculate()

    def handle_clear(self):
        self.clear_display()

class MiniApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мини приложение")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        # Кнопка для калькулятора
        calculator_button = QPushButton("Калькулятор")
        calculator_button.clicked.connect(self.open_calculator)
        layout.addWidget(calculator_button)

        # Кнопка для секундомера
        self.timer_lcd = QLCDNumber()
        self.timer_lcd.setDigitCount(8)
        layout.addWidget(self.timer_lcd)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.start_button = QPushButton("Старт")
        self.start_button.clicked.connect(self.start_timer)
        layout.addWidget(self.start_button)

        # Кнопка для таймера
        self.timer_label = QLabel("Таймер:")
        layout.addWidget(self.timer_label)

        self.timer_edit = QLineEdit()
        layout.addWidget(self.timer_edit)

        self.set_timer_button = QPushButton("Установить")
        self.set_timer_button.clicked.connect(self.set_timer)
        layout.addWidget(self.set_timer_button)

        self.setLayout(layout)

        self.calculator_window = None  # Создаем атрибут для хранения экземпляра окна калькулятора

    def open_calculator(self):
        if not self.calculator_window:
            self.calculator_window = CalculatorWindow()
            self.calculator_window.show()
        else:
            self.calculator_window.show()
    def open_calculator(self):
        if not self.calculator_window:
            self.calculator_window = CalculatorWindow()
            self.calculator_window.show()
        else:
            self.calculator_window.show()

    def start_timer(self):
        self.timer.start(1000)  # Запускаем таймер, обновление каждую секунду

    def update_timer(self):
        time = self.timer_lcd.value()
        time += 1
        self.timer_lcd.display(time)

    def set_timer(self):
        try:
            time = int(self.timer_edit.text())
            self.timer_lcd.display(time)
        except ValueError:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MiniApp()
    window.show()
    sys.exit(app.exec_())
