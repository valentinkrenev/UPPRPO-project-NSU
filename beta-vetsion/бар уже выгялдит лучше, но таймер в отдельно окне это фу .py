import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QLCDNumber, QDialog, QGridLayout, QHBoxLayout, QFrame
from PyQt5.QtCore import QTimer, Qt

class CalculatorWindow(QWidget):
    def __init__(self):
        super().__init__()
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
            button.setFixedSize(40, 40)  # Устанавливаем фиксированный размер кнопок
            buttons_layout.addWidget(button, *pos)
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

class AppSelectionWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.calculator_button = QPushButton("Калькулятор")
        self.calculator_button.setFixedSize(100, 30)  # Устанавливаем фиксированный размер кнопок
        layout.addWidget(self.calculator_button)

        self.timer_button = QPushButton("Таймер")
        self.timer_button.setFixedSize(100, 30)  # Устанавливаем фиксированный размер кнопок
        layout.addWidget(self.timer_button)

        self.setLayout(layout)

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.app_selection_widget = AppSelectionWidget()
        self.calculator_window = CalculatorWindow()
        self.timer_window = TimerWindow()

        main_layout = QHBoxLayout()

        main_layout.addWidget(self.app_selection_widget)
        main_layout.addWidget(self.calculator_window)  # По умолчанию показываем окно калькулятора

        self.setLayout(main_layout)

        self.app_selection_widget.calculator_button.clicked.connect(self.show_calculator)
        self.app_selection_widget.timer_button.clicked.connect(self.show_timer)

    def show_calculator(self):
        self.calculator_window.show()
        self.timer_window.hide()

    def show_timer(self):
        self.calculator_window.hide()
        self.timer_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())
