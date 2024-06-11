import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLCDNumber, QGridLayout, QHBoxLayout, QStackedWidget
from PyQt5.QtCore import QTimer, Qt, QSettings
from PyQt5.QtGui import QFont, QIcon

# Button style for both themes
button_style = {
    "dark": """
        QPushButton {
            background-color: #2E2E2E;
            border: 2px solid #888888;
            color: white;
            padding: 15px;
            font-size: 18px;
            border-radius: 8px;
            font-weight: bold;
            margin: 4px;
            box-shadow: 2px 2px 5px #888888;
        }

        QPushButton:hover {
            background-color: #3E3E3E;
        }

        QPushButton:pressed {
            background-color: #1E1E1E;
        }
    """,
    "light": """
        QPushButton {
            background-color: #F0F0F0;
            border: 2px solid #888888;
            color: black;
            padding: 15px;
            font-size: 18px;
            border-radius: 8px;
            font-weight: bold;
            margin: 4px;
            box-shadow: 2px 2px 5px #888888;
        }

        QPushButton:hover {
            background-color: #E0E0E0;
        }

        QPushButton:pressed {
            background-color: #C0C0C0;
        }
    """
}

# Window style for both themes
window_style = {
    "dark": """
        QWidget {
            background-color: #1E1E1E;
        }
        QLineEdit {
            background-color: #2E2E2E;
            color: #FFFFFF;
            font-size: 28px;
            border: none;
            padding: 10px;
        }
        QLCDNumber {
            background-color: #2E2E2E;
            color: #FFFFFF;
            border: none;
            font-size: 24px;
        }
    """,
    "light": """
        QWidget {
            background-color: #FFFFFF;
        }
        QLineEdit {
            background-color: #F0F0F0;
            color: #000000;
            font-size: 28px;
            border: none;
            padding: 10px;
        }
        QLCDNumber {
            background-color: #F0F0F0;
            color: #000000;
            border: none;
            font-size: 24px;
        }
    """
}

class CalculatorWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        layout = QVBoxLayout()

        self.result_display = QLineEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        buttons_layout = QGridLayout()

        buttons = [
            ("7", (0, 0)), ("8", (0, 1)), ("9", (0, 2)), ("/", (0, 3)),
            ("4", (1, 0)), ("5", (1, 1)), ("6", (1, 2)), ("*", (1, 3)),
            ("1", (2, 0)), ("2", (2, 1)), ("3", (2, 2)), ("-", (2, 3)),
            ("0", (3, 0)), (".", (3, 1)), ("=", (3, 2)), ("+", (3, 3)),
            ("C", (4, 0, 1, 3)), ("Close", (4, 3, 1, 1)),
        ]

        for button_text, pos in buttons:
            button = QPushButton(button_text)
            if button_text == "Close":
                button.setStyleSheet("background-color: #D32F2F; font-size: 18px; font-weight: bold; color: white;")
                button.clicked.connect(self.close)
            else:
                buttons_layout.addWidget(button, *pos)
                if button_text != '=' and button_text != 'C':
                    button.clicked.connect(lambda _, text=button_text: self.update_display(text))
                elif button_text == '=':
                    button.clicked.connect(self.handle_equal)
                else:
                    button.clicked.connect(self.handle_clear)

            button.setStyleSheet(self.parent.get_button_style())

        layout.addLayout(buttons_layout)
        self.setLayout(layout)
        self.update_styles()

        self.calculation_to_eval = ""

    def update_styles(self):
        self.setStyleSheet(self.parent.get_window_style())
        for btn in self.findChildren(QPushButton):
            if btn.text() != "Close":
                btn.setStyleSheet(self.parent.get_button_style())

    def update_display(self, value):
        self.calculation_to_eval += value
        self.result_display.setText(self.calculation_to_eval)

    def calculate(self):
        try:
            result = eval(self.calculation_to_eval)
            self.result_display.setText(str(result))
            self.calculation_to_eval = ""
        except Exception:
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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        layout = QVBoxLayout()

        self.timer_lcd = QLCDNumber()
        self.timer_lcd.setDigitCount(11)
        layout.addWidget(self.timer_lcd)

        buttons_layout = QHBoxLayout()

        self.start_button = QPushButton("Старт")
        self.start_button.setStyleSheet(button_style["dark"])
        self.start_button.clicked.connect(self.start_timer)
        buttons_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Стоп")
        self.stop_button.setStyleSheet(button_style["dark"])
        self.stop_button.clicked.connect(self.stop_timer)
        buttons_layout.addWidget(self.stop_button)

        self.reset_button = QPushButton("Сброс")
        self.reset_button.setStyleSheet(button_style["dark"])
        self.reset_button.clicked.connect(self.reset_timer)
        buttons_layout.addWidget(self.reset_button)

        layout.addLayout(buttons_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.time_elapsed = 0
        self.is_running = False
        self.setLayout(layout)
        self.update_styles()

    def update_styles(self):
        self.setStyleSheet(self.parent.get_window_style())
        self.start_button.setStyleSheet(self.parent.get_button_style())
        self.stop_button.setStyleSheet(self.parent.get_button_style())
        self.reset_button.setStyleSheet(self.parent.get_button_style())

    def start_timer(self):
        if not self.is_running:
            self.timer.start(10)
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
        time_str = "{:02d}:{:02d}.{:02d}".format(
            (self.time_elapsed // 6000) % 60,
            (self.time_elapsed // 100) % 60,
            self.time_elapsed % 100
        )
        self.timer_lcd.display(time_str)

class AppSelectionWidget(QWidget):
    def __init__(self, stacked_widget, parent):
        super().__init__()

        self.parent = parent

        layout = QVBoxLayout()

        self.calculator_button = QPushButton("Калькулятор")
        self.calculator_button.setFixedSize(200, 50)
        self.calculator_button.setStyleSheet(self.parent.get_button_style())
        layout.addWidget(self.calculator_button)

        self.timer_button = QPushButton("Секундамер")
        self.timer_button.setFixedSize(200, 50)
        self.timer_button.setStyleSheet(self.parent.get_button_style())
        layout.addWidget(self.timer_button)

        self.theme_button = QPushButton("Сменить тему")
        self.theme_button.setFixedSize(200, 50)
        self.theme_button.setStyleSheet(self.parent.get_button_style())
        layout.addWidget(self.theme_button)

        self.setLayout(layout)

        self.calculator_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
        self.timer_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))
        self.theme_button.clicked.connect(self.parent.toggle_theme)

    def update_styles(self):
        self.calculator_button.setStyleSheet(self.parent.get_button_style())
        self.timer_button.setStyleSheet(self.parent.get_button_style())
        self.theme_button.setStyleSheet(self.parent.get_button_style())

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MHAap")
        # self.setWindowIcon(QIcon("icon.png"))  # Replace with your icon file path

        self.settings = QSettings("MyCompany", "MyApp")
        self.theme = self.settings.value("theme", "dark")

        self.stacked_widget = QStackedWidget()

        self.calculator_window = CalculatorWindow(self)
        self.timer_window = TimerWindow(self)

        self.stacked_widget.addWidget(self.calculator_window)
        self.stacked_widget.addWidget(self.timer_window)

        main_layout = QHBoxLayout()

        self.app_selection_widget = AppSelectionWidget(self.stacked_widget, self)
        main_layout.addWidget(self.app_selection_widget)
        main_layout.addWidget(self.stacked_widget)

        self.setLayout(main_layout)
        self.update_styles()

    def get_button_style(self):
        return button_style[self.theme]

    def get_window_style(self):
        return window_style[self.theme]

    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.settings.setValue("theme", self.theme)
        self.update_styles()

    def update_styles(self):
        self.calculator_window.update_styles()
        self.timer_window.update_styles()
        self.app_selection_widget.update_styles()
        self.setStyleSheet(self.get_window_style())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())
