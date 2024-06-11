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
            self.timer.stop
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
            self.time_elapsed % 100,
        )
        self.timer_lcd.display(time_str)

class NotesWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        layout = QVBoxLayout()

        self.notes_text_edit = QTextEdit()
        layout.addWidget(self.notes_text_edit)

        self.save_button = QPushButton("Сохранить")
        self.save_button.setStyleSheet(button_style["dark"])
        self.save_button.clicked.connect(self.save_notes)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.update_styles()
        self.load_notes()

    def update_styles(self):
        self.setStyleSheet(self.parent.get_window_style())
        self.save_button.setStyleSheet(self.parent.get_button_style())

    def save_notes(self):
        with open("notes.txt", "w") as file:
            file.write(self.notes_text_edit.toPlainText())

    def load_notes(self):
        if os.path.exists("notes.txt"):
            with open("notes.txt", "r") as file:
                self.notes_text_edit.setPlainText(file.read())

class ClickerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        layout = QVBoxLayout()

        self.click_count = 0

        self.click_display = QLabel("Нажатий: 0")
        self.click_display.setFont(QFont("Arial", 24))
        layout.addWidget(self.click_display)

        self.click_button = QPushButton("Нажми меня")
        self.click_button.setStyleSheet(button_style["dark"])
        self.click_button.setFixedSize(100, 100)
        self.click_button.setStyleSheet("border-radius: 50px;")
        self.click_button.clicked.connect(self.increment_click)
        layout.addWidget(self.click_button)

        self.setLayout(layout)
        self.update_styles()

    def update_styles(self):
        self.setStyleSheet(self.parent.get_window_style())
        self.click_button.setStyleSheet(self.parent.get_button_style() + "border-radius: 50px;")

    def increment_click(self):
        self.click_count += 1
        self.click_display.setText(f"Нажатий: {self.click_count}")

class RandomizerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        layout = QVBoxLayout()

        self.min_label = QLabel("Минимум:")
        layout.addWidget(self.min_label)

        self.min_input = QSpinBox()
        self.min_input.setMinimum(0)
        layout.addWidget(self.min_input)

        self.max_label = QLabel("Максимум:")
        layout.addWidget(self.max_label)

        self.max_input = QSpinBox()
        self.max_input.setMaximum(1000)
        layout.addWidget(self.max_input)

        self.generate_button = QPushButton("Генерировать")
        self.generate_button.setStyleSheet(button_style["dark"])
        self.generate_button.clicked.connect(self.generate_random)
        layout.addWidget(self.generate_button)

        self.result_display = QLabel("Результат:")
        self.result_display.setFont(QFont("Arial", 24))
        layout.addWidget(self.result_display)

        self.coin_button = QPushButton("Подбросить монетку")
        self.coin_button.setStyleSheet(button_style["dark"])
        self.coin_button.clicked.connect(self.flip_coin)
        layout.addWidget(self.coin_button)

        self.coin_result_display = QLabel("Монетка:")
        self.coin_result_display.setFont(QFont("Arial", 24))
        layout.addWidget(self.coin_result_display)

        self.setLayout(layout)
        self.update_styles()

    def update_styles(self):
        self.setStyleSheet(self.parent.get_window_style())
        self.generate_button.setStyleSheet(self.parent.get_button_style())
        self.coin_button.setStyleSheet(self.parent.get_button_style())

    def generate_random(self):
        min_value = self.min_input.value()
        max_value = self.max_input.value()
        random_value = random.randint(min_value, max_value)
        self.result_display.setText(f"Результат: {random_value}")

    def flip_coin(self):
        coin_result = random.choice(["0", "1"])
        self.coin_result_display.setText(f"Монетка: {coin_result}")

class AppSelectionWidget(QWidget):
    def __init__(self, stacked_widget, parent):
        super().__init__()

        self.parent = parent

        layout = QVBoxLayout()

        self.calculator_button = QPushButton("Калькулятор")
        self.calculator_button.setFixedSize(150, 50)
        layout.addWidget(self.calculator_button)

        self.timer_button = QPushButton("Секундомер")
        self.timer_button.setFixedSize(150, 50)
        layout.addWidget(self.timer_button)

        self.notes_button = QPushButton("Заметки")
        self.notes_button.setFixedSize(150, 50)
        layout.addWidget(self.notes_button)

        self.clicker_button = QPushButton("Кликер")
        self.clicker_button.setFixedSize(150, 50)
        layout.addWidget(self.clicker_button)

        self.randomizer_button = QPushButton("Рандомайзер")
        self.randomizer_button.setFixedSize(150, 50)
        layout.addWidget(self.randomizer_button)

        self.theme_button = QPushButton("Тема")
        self.theme_button.setFixedSize(150, 50)
        layout.addWidget(self.theme_button)

        self.always_on_top_checkbox = QCheckBox("Всегда поверх")
        self.always_on_top_checkbox.setChecked(self.parent.isAlwaysOnTop())
        layout.addWidget(self.always_on_top_checkbox)

        self.setLayout(layout)

        self.calculator_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
        self.timer_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))
        self.notes_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(2))
        self.clicker_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(3))
        self.randomizer_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(4))
        self.theme_button.clicked.connect(self.parent.toggle_theme)
        self.always_on_top_checkbox.stateChanged.connect(self.parent.toggle_always_on_top)

        self.update_styles()

    def update_styles(self):
        self.setStyleSheet(self.parent.get_window_style())
        self.calculator_button.setStyleSheet(self.parent.get_button_style())
        self.timer_button.setStyleSheet(self.parent.get_button_style())
        self.notes_button.setStyleSheet(self.parent.get_button_style())
        self.clicker_button.setStyleSheet(self.parent.get_button_style())
        self.randomizer_button.setStyleSheet(self.parent.get_button_style())
        self.theme_button.setStyleSheet(self.parent.get_button_style())
        self.always_on_top_checkbox.setStyleSheet(self.parent.get_button_style())

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Многофункциональное приложение")
        self.setWindowIcon(QIcon('app_icon.png'))

        self.settings = QSettings("MyApp", "AppSettings")
        self.theme = self.settings.value("theme", "light")

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
        self.setWindowFlags(Qt.WindowStaysOnTopHint if self.settings.value("always_on_top", False, type=bool) else Qt.Widget)
        self.update_styles()

    def create_menu_bar(self):
        self.menu_bar = QMenuBar()

        self.language_menu = self.menu_bar.addMenu("Язык")

        self.english_action = QAction("Английский", self)
        self.russian_action = QAction("Русский", self)
        
        self.english_action.triggered.connect(lambda: self.change_language("en"))
        self.russian_action.triggered.connect(lambda: self.change_language("ru"))

        self.language_menu.addAction(self.english_action)
        self.language_menu.addAction(self.russian_action)

        return self.menu_bar

    def change_language(self, language):
        if language == "en":
            self.setWindowTitle("Multifunctional Application")
            self.language_menu.setTitle("Language")
            self.english_action.setText("English")
            self.russian_action.setText("Russian")
            self.app_selection_widget.calculator_button.setText("Calculator")
            self.app_selection_widget.timer_button.setText("Stopwatch")
            self.app_selection_widget.notes_button.setText("Notes")
            self.app_selection_widget.clicker_button.setText("Clicker")
            self.app_selection_widget.randomizer_button.setText("Randomizer")
            self.app_selection_widget.theme_button.setText("Theme")
            self.app_selection_widget.always_on_top_checkbox.setText("Always on Top")
            self.calculator_window.update_display("")

        elif language == "ru":
            self.setWindowTitle("Многофункциональное приложение")
            self.language_menu.setTitle("Язык")
            self.english_action.setText("Английский")
            self.russian_action.setText("Русский")
            self.app_selection_widget.calculator_button.setText("Калькулятор")
            self.app_selection_widget.timer_button.setText("Секундомер")
            self.app_selection_widget.notes_button.setText("Заметки")
            self.app_selection_widget.clicker_button.setText("Кликер")
            self.app_selection_widget.randomizer_button.setText("Рандомайзер")
            self.app_selection_widget.theme_button.setText("Тема")
            self.app_selection_widget.always_on_top_checkbox.setText("Всегда поверх")
            self.calculator_window.update_display("")

    def toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
        else:
            self.theme = "light"
        self.settings.setValue("theme", self.theme)
        self.update_styles()

    def toggle_always_on_top(self, state):
        self.setWindowFlags(Qt.WindowStaysOnTopHint if state == Qt.Checked else Qt.Widget)
        self.show()
        self.settings.setValue("always_on_top", state == Qt.Checked)

    def isAlwaysOnTop(self):
        return self.settings.value("always_on_top", False, type=bool)

    def get_button_style(self):
        return button_style[self.theme]

    def get_window_style(self):
        return window_style[self.theme]

    def update_styles(self):
        self.setStyleSheet(self.get_window_style())
        self.app_selection_widget.update_styles()
        self.calculator_window.update_styles()
        self.timer_window.update_styles()
        self.notes_window.update_styles()
        self.clicker_window.update_styles()
        self.randomizer_window.update_styles()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())
