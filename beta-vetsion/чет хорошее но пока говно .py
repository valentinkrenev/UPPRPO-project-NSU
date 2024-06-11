import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLCDNumber, QGridLayout, QHBoxLayout, QFrame, QStackedWidget
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
            ("Close", (4, 3, 1, 1)),  # Close button added
        ]

        for button_text, pos in buttons:
            button = QPushButton(button_text)
            if button_text == "Close":
                button.setStyleSheet("background-color: red")  # Setting button color to red
                button.clicked.connect(self.close)  # Connect close function to Close button
            else:
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
        self.timer_lcd.setDigitCount(11)  # Устанавливаем количество цифр для отображения миллисекунд
        layout.addWidget(self.timer_lcd)

        buttons_layout = QHBoxLayout()

        self.start_button = QPushButton("Старт")
        self.start_button.clicked.connect(self.start_timer)
        buttons_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Стоп")
        self.stop_button.clicked.connect(self.stop_timer)
        buttons_layout.addWidget(self.stop_button)

        self.reset_button = QPushButton("Сброс")
        self.reset_button.clicked.connect(self.reset_timer)
        buttons_layout.addWidget(self.reset_button)

        layout.addLayout(buttons_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.time_elapsed = 0
        self.is_running = False
        self.setLayout(layout)

    def start_timer(self):
        if not self.is_running:
            self.timer.start(10)  # Устанавливаем интервал в 10 миллисекунд
            self.is_running = True
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)

    def stop_timer(self):
        if self.is_running:
            self.timer.stop()
            self.is_running = False
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def reset_timer(self):
        self.time_elapsed = 0
        self.update_display()

    def update_timer(self):
        self.time_elapsed += 1
        self.update_display()

    def update_display(self):
        # Преобразуем время в миллисекундах в строку для отображения на дисплее
        time_str = "{:02d}:{:02d}.{:02d}".format(
            (self.time_elapsed // 6000) % 60,  # Минуты
            (self.time_elapsed // 100) % 60,   # Секунды
            self.time_elapsed % 100            # Миллисекунды
        )
        self.timer_lcd.display(time_str)

class AppSelectionWidget(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        layout = QVBoxLayout()

        self.calculator_button = QPushButton("Калькулятор")
        self.calculator_button.setFixedSize(100, 30)  # Устанавливаем фиксированный размер кнопок
        layout.addWidget(self.calculator_button)

        self.timer_button = QPushButton("Таймер")
        self.timer_button.setFixedSize(100, 30)  # Устанавливаем фиксированный размер кнопок
        layout.addWidget(self.timer_button)

        self.setLayout(layout)

        self.calculator_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
        self.timer_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.stacked_widget = QStackedWidget()

        self.calculator_window = CalculatorWindow()
        self.timer_window = TimerWindow()

        self.stacked_widget.addWidget(self.calculator_window)
        self.stacked_widget.addWidget(self.timer_window)

        main_layout = QHBoxLayout()

        self.app_selection_widget = AppSelectionWidget(self.stacked_widget)
        main_layout.addWidget(self.app_selection_widget)
        main_layout.addWidget(self.stacked_widget)

        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())
