import sys
import os
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLCDNumber, QGridLayout, 
                             QHBoxLayout, QStackedWidget, QTextEdit, QLabel, QMenuBar, QAction, QCheckBox, QSpinBox)
from PyQt5.QtCore import QTimer, Qt, QSettings
from PyQt5.QtGui import QFont, QIcon

# Стиль кнопок для обеих тем
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
        }

        QPushButton:hover {
            background-color: #E0E0E0;
        }

        QPushButton:pressed {
            background-color: #C0C0C0;
        }
    """
}

# Стиль окна и флажка для обеих тем
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
        QTextEdit {
            background-color: #2E2E2E;
            color: #FFFFFF;
            font-size: 18px;
            border: 1px solid #888888;
            padding: 10px;
        }
        QCheckBox {
            color: #FFFFFF;
            font-size: 18px;
        }
        QMenuBar {
            background-color: #2E2E2E;
            color: #FFFFFF;
        }
        QMenu {
            background-color: #2E2E2E;
            color: #FFFFFF;
        }
        QMenu::item {
            background-color: #2E2E2E;
            color: #FFFFFF;
        }
        QMenu::item:selected {
            background-color: #3E3E3E;
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
        QTextEdit {
            background-color: #FFFFFF;
            color: #000000;
            font-size: 18px;
            border: 1px solid #888888;
            padding: 10px;
        }
        QCheckBox {
            color: #000000;
            font-size: 18px;
        }
        QMenuBar {
            background-color: #F0F0F0;
            color: #000000;
        }
        QMenu {
            background-color: #F0F0F0;
            color: #000000;
        }
        QMenu::item {
            background-color: #F0F0F0;
            color: #000000;
        }
        QMenu::item:selected {
            background-color: #E0E0E0;
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
        self.timer.stop()
        self.time_elapsed = 0
        self.timer_lcd.display("00:00:00:00")
        self.is_running = False
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_timer(self):
        self.time_elapsed += 1
        time_str = "{:02d}:{:02d}:{:02d}:{:02d}".format(
            self.time_elapsed // 360000,
            (self.time_elapsed // 6000) % 60,
            (self.time_elapsed // 100) % 60,
            self.time_elapsed % 100
        )
        self.timer_lcd.display(time_str)

class NotesWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        layout = QVBoxLayout()

        self.notes_edit = QTextEdit()
        self.notes_edit.setFont(QFont("Arial", 14))
        layout.addWidget(self.notes_edit)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_notes)
        layout.addWidget(self.save_button)

        self.load_button = QPushButton("Загрузить")
        self.load_button.clicked.connect(self.load_notes)
        layout.addWidget(self.load_button)

        self.setLayout(layout)
        self.update_styles()

    def update_styles(self):
        self.setStyleSheet(self.parent.get_window_style())
        self.save_button.setStyleSheet(self.parent.get_button_style())
        self.load_button.setStyleSheet(self.parent.get_button_style())

    def save_notes(self):
        notes_text = self.notes_edit.toPlainText()
        with open("notes.txt", "w") as file:
            file.write(notes_text)

    def load_notes(self):
        if os.path.exists("notes.txt"):
            with open("notes.txt", "r") as file:
                notes_text = file.read()
                self.notes_edit.setText(notes_text)

class ClickerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.click_count = 0

        self.click_display = QLabel()
        self.click_display.setFont(QFont("Arial", 24))

        self.click_button = QPushButton()
        self.click_button.setFixedSize(100, 100)
        self.click_button.setStyleSheet("border-radius: 50px;")
        self.click_button.clicked.connect(self.increment_click)

        layout = QVBoxLayout()
        layout.addWidget(self.click_display)
        layout.addWidget(self.click_button)
        self.setLayout(layout)
        self.update_styles()
        self.update_language()

    def update_styles(self):
        self.setStyleSheet(self.parent.get_window_style())
        self.click_button.setStyleSheet(self.parent.get_button_style() + "border-radius: 50px;")
        if self.parent.theme == "dark":
            self.click_display.setStyleSheet("color: white;")
        else:
            self.click_display.setStyleSheet("color: black;")

    def update_language(self):
        self.click_display.setText(f"{'Clicks' if self.parent.language == 'en' else 'Нажатий'}: {self.click_count}")
        self.click_button.setText("Click Me" if self.parent.language == "en" else "Нажми меня")

    def increment_click(self):
        self.click_count += 1
        self.click_display.setText(f"{'Clicks' if self.parent.language == 'en' else 'Нажатий'}: {self.click_count}")


class RandomizerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.min_label = QLabel()
        self.min_input = QSpinBox()
        self.min_input.setMinimum(0)

        self.max_label = QLabel()
        self.max_input = QSpinBox()
        self.max_input.setMaximum(1000)

        self.generate_button = QPushButton()
        self.generate_button.clicked.connect(self.generate_random)

        self.result_display = QLabel()
        self.result_display.setFont(QFont("Arial", 24))

        self.coin_button = QPushButton()
        self.coin_button.clicked.connect(self.flip_coin)

        self.coin_result_display = QLabel()
        self.coin_result_display.setFont(QFont("Arial", 24))

        layout = QVBoxLayout()
        layout.addWidget(self.min_label)
        layout.addWidget(self.min_input)
        layout.addWidget(self.max_label)
        layout.addWidget(self.max_input)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.result_display)
        layout.addWidget(self.coin_button)
        layout.addWidget(self.coin_result_display)
        self.setLayout(layout)
        self.update_styles()
        self.update_language()

    def update_styles(self):
        self.setStyleSheet(self.parent.get_window_style())
        self.generate_button.setStyleSheet(self.parent.get_button_style())
        self.coin_button.setStyleSheet(self.parent.get_button_style())
        if self.parent.theme == "dark":
            self.min_label.setStyleSheet("color: white;")
            self.max_label.setStyleSheet("color: white;")
            self.result_display.setStyleSheet("color: white;")
            self.coin_result_display.setStyleSheet("color: white;")
        else:
            self.min_label.setStyleSheet("color: black;")
            self.max_label.setStyleSheet("color: black;")
            self.result_display.setStyleSheet("color: black;")
            self.coin_result_display.setStyleSheet("color: black;")

    def update_language(self):
        if self.parent.language == "en":
            self.min_label.setText("Minimum:")
            self.max_label.setText("Maximum:")
            self.generate_button.setText("Generate")
            self.result_display.setText("Result:")
            self.coin_button.setText("Flip Coin")
            self.coin_result_display.setText("Coin:")
        else:
            self.min_label.setText("Минимум:")
            self.max_label.setText("Максимум:")
            self.generate_button.setText("Генерировать")
            self.result_display.setText("Результат:")
            self.coin_button.setText("Подбросить монетку")
            self.coin_result_display.setText("Монетка:")

    def generate_random(self):
        min_value = self.min_input.value()
        max_value = self.max_input.value()
        random_value = random.randint(min_value, max_value)
        self.result_display.setText(f"{'Result' if self.parent.language == 'en' else 'Результат'}: {random_value}")

    def flip_coin(self):
        coin_result = random.choice(["Heads" if self.parent.language == "en" else "Орел", "Tails" if self.parent.language == "en" else "Решка"])
        self.coin_result_display.setText(f"{'Coin' if self.parent.language == 'en' else 'Монетка'}: {coin_result}")

class AppSelectionWidget(QWidget):
    def __init__(self, stacked_widget, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.stacked_widget = stacked_widget

        self.calculator_button = QPushButton()
        self.timer_button = QPushButton()
        self.notes_button = QPushButton()
        self.clicker_button = QPushButton()
        self.randomizer_button = QPushButton()

        self.theme_button = QPushButton()
        self.theme_button.clicked.connect(self.parent.toggle_theme)

        self.always_on_top_checkbox = QCheckBox()
        self.always_on_top_checkbox.setChecked(self.parent.isAlwaysOnTop())
        self.always_on_top_checkbox.stateChanged.connect(self.parent.toggle_always_on_top)

        self.calculator_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.timer_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.notes_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.clicker_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.randomizer_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))

        layout = QVBoxLayout()
        layout.addWidget(self.calculator_button)
        layout.addWidget(self.timer_button)
        layout.addWidget(self.notes_button)
        layout.addWidget(self.clicker_button)
        layout.addWidget(self.randomizer_button)
        layout.addWidget(self.theme_button)
        layout.addWidget(self.always_on_top_checkbox)
        self.setLayout(layout)
        self.update_styles()
        self.update_language()

    def update_styles(self):
        self.setStyleSheet(self.parent.get_window_style())
        self.calculator_button.setStyleSheet(self.parent.get_button_style())
        self.timer_button.setStyleSheet(self.parent.get_button_style())
        self.notes_button.setStyleSheet(self.parent.get_button_style())
        self.clicker_button.setStyleSheet(self.parent.get_button_style())
        self.randomizer_button.setStyleSheet(self.parent.get_button_style())
        self.theme_button.setStyleSheet(self.parent.get_button_style())

    def update_language(self):
        if self.parent.language == "en":
            self.calculator_button.setText("Calculator")
            self.timer_button.setText("Stopwatch")
            self.notes_button.setText("Notes")
            self.clicker_button.setText("Clicker")
            self.randomizer_button.setText("Randomizer")
            self.theme_button.setText("Theme")
            self.always_on_top_checkbox.setText("Always on Top")
        else:
            self.calculator_button.setText("Калькулятор")
            self.timer_button.setText("Секундомер")
            self.notes_button.setText("Заметки")
            self.clicker_button.setText("Кликер")
            self.randomizer_button.setText("Рандомайзер")
            self.theme_button.setText("Тема")
            self.always_on_top_checkbox.setText("Всегда поверх")

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Многофункциональное приложение")
        self.setWindowIcon(QIcon('app_icon.png'))

        self.settings = QSettings("MyApp", "AppSettings")
        self.theme = self.settings.value("theme", "light")
        self.language = self.settings.value("language", "ru")

        self.stacked_widget = QStackedWidget()

        self.calculator_window = CalculatorWindow(self)
        self.timer_window = TimerWindow(self)
        self.notes_window = NotesWindow(self)
        self.clicker_window = ClickerWindow(self)
        self.randomizer_window = RandomizerWindow(self)

        self.stacked_widget.addWidget(self.calculator_window)
        self.stacked_widget.addWidget(self.timer_window)
        self.stacked_widget.addWidget(self.notes_window)
        self.stacked_widget.addWidget(self.clicker_window)
        self.stacked_widget.addWidget(self.randomizer_window)

        main_layout = QVBoxLayout()

        self.app_selection_widget = AppSelectionWidget(self.stacked_widget, self)
        
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.app_selection_widget)
        top_layout.addWidget(self.stacked_widget)

        main_layout.setMenuBar(self.create_menu_bar())
        main_layout.addLayout(top_layout)

        self.setLayout(main_layout)
        self.update_styles()

    def update_styles(self):
        self.setStyleSheet(self.get_window_style())
        self.app_selection_widget.update_styles()
        self.calculator_window.update_styles()
        self.timer_window.update_styles()
        self.notes_window.update_styles()
        self.clicker_window.update_styles()
        self.randomizer_window.update_styles()

    def update_language(self):
        self.app_selection_widget.update_language()
        self.clicker_window.update_language()
        self.randomizer_window.update_language()

    def create_menu_bar(self):
        self.menu_bar = QMenuBar()

        self.language_menu = self.menu_bar.addMenu("Язык")

        self.english_action = QAction("Английский", self)
        self.russian_action = QAction("Русский", self)
        
        self.english_action.triggered.connect(lambda: self.toggle_language("en"))
        self.russian_action.triggered.connect(lambda: self.toggle_language("ru"))

        self.language_menu.addAction(self.english_action)
        self.language_menu.addAction(self.russian_action)

        return self.menu_bar

    def toggle_language(self, lang=None):
        if lang:
            self.language = lang
        else:
            self.language = "en" if self.language == "ru" else "ru"
        self.settings.setValue("language", self.language)
        self.update_language()

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.settings.setValue("theme", self.theme)
        self.update_styles()
    
    def toggle_always_on_top(self, state):
        self.setWindowFlag(Qt.WindowStaysOnTopHint, state == Qt.Checked)
        self.show()

    def get_button_style(self):
        return button_style[self.theme]

    def get_window_style(self):
        return window_style[self.theme]

    def isAlwaysOnTop(self):
        return self.windowFlags() & Qt.WindowStaysOnTopHint != 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = AppWindow()
    main_window.show()
    sys.exit(app.exec_())
