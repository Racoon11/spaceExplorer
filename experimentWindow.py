from PyQt6.QtWidgets import QMessageBox, QMainWindow, QVBoxLayout, QListWidgetItem, QFrame, QSplitter, QSizePolicy
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import random
import os
import sys

from importDataWindow import *

class ChartItemWidget(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Заголовок
        self.label = QLabel(title)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        # График
        self.figure = Figure(figsize=(5, 1.5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        layout.addWidget(self.canvas)

        self.plot()

    def plot(self):
        ax = self.figure.add_subplot(111)
        ax.clear()
        data = [random.random() for _ in range(10)]
        times = list(range(10))
        ax.plot(times, data, label="Данные")
        # ax.set_title("График")
        ax.set_xlabel("Время")
        ax.legend()
        ax.grid(True)
        self.canvas.draw()

    def resizeEvent(self, event):
        """Перерисовываем график при изменении размера виджета"""
        self.canvas.resize(event.size())
        self.canvas.draw()

# Основное окно
class ExperimentWindow(QMainWindow):
    def __init__(self, a, b):
        super().__init__()

        self.setWindowTitle("Список с графиками")
        # self.setGeometry(200, 200, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        left_panel = QVBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.setMinimumWidth(400)  # Минимальная ширина левой части

        titles = ["Элемент 1", "Элемент 2", "Элемент 3", "Элемент 4", "Элемент 5"]

        for title in titles:
            item = QListWidgetItem(self.list_widget)
            widget = ChartItemWidget(title)
            item.setSizeHint(widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)

        left_panel.addWidget(self.list_widget)

        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: white;")
        right_panel.setFrameShape(QFrame.Shape.Box)
        right_panel.setLineWidth(1)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.list_widget)
        splitter.addWidget(right_panel)

        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter)

        main_widget.setLayout(layout)
        self.create_menu()

    def create_menu(self):
        # Получаем строку меню
        menu_bar = self.menuBar()

        # ==== Меню "Файл" ====
        menu_data = menu_bar.addMenu("Данные")

        data_action = menu_data.addAction("Датчики")
        data_action.triggered.connect(self.show_data_window)

        video_action = menu_data.addAction("Видео")
        sound_action = menu_data.addAction("Звук")
        # file_menu = menu_bar.addMenu("Данные")

        # self.file_submenu = file_menu.addMenu('Тип данных')
        # button_action = self.file_submenu.addAction("Голова") 
        # # button_action.triggered.connect(partial(self.change_type, new_type="Голова"))
        # # button_action = self.file_submenu.addAction("Шея") 
        # button_action = self.file_submenu.addAction("Грудная клетка")
        # button_action = self.file_submenu.addAction("Голень") 
        # button_action = self.file_submenu.addAction("Аудио") 
         
        # self.file_submenu.triggered.connect(self.on_menu_item_clicked)

        # # Действие "Открыть"
        # open_action = file_menu.addAction("Открыть")
        # open_action.triggered.connect(self.open_file)

        # # Действие "Сохранить"
        # save_action = file_menu.addAction("Сохранить")
        # save_action.triggered.connect(self.save_file)

        # # Разделитель
        # file_menu.addSeparator()

        # # Действие "Выход"
        # exit_action = file_menu.addAction("Выход")
        # exit_action.triggered.connect(self.close)

        # ==== Меню "Помощь" ====
        help_menu = menu_bar.addMenu("Помощь")

        # Действие "О программе"
        about_action = help_menu.addAction("О программе")
        about_action.triggered.connect(self.about_program)
    

    def show_data_window(self):
        self.new_window = ImportDataWindow()
        self.new_window.show()
    
    def about_program(self):
        QMessageBox.about(self, "О программе", "Это простое приложение с меню на PyQt6")

# class ExperimentWindow(QMainWindow):
#     def __init__(self, name, path):
#         super().__init__()

#         self.setWindowTitle("Список с графиками")
#         self.resize(800, 600)

#         # Главной виджет
#         main_widget = QWidget()
#         self.setCentralWidget(main_widget)
#         layout = QHBoxLayout(main_widget)

#         # Левая панель со списком
#         left_panel = QVBoxLayout()

#         self.list_widget = QListWidget()
#         self.list_widget.setLineWidth(1)

#         titles = ["Элемент 1", "Элемент 2", "Элемент 3", "Элемент 4", "Элемент 5"]

#         for title in titles:
#             item = QListWidgetItem(self.list_widget)
#             widget = ChartItemWidget(title)
#             item.setSizeHint(widget.sizeHint())
#             self.list_widget.addItem(item)
#             self.list_widget.setItemWidget(item, widget)

#         left_panel.addWidget(self.list_widget)

#         # Правая панель (пока пустая)
#         right_panel = QFrame()
#         right_panel.setStyleSheet("background-color: white;")
#         right_panel.setFrameShape(QFrame.Shape.Box)
#         right_panel.setLineWidth(1)

#         # Разделение окна
#         splitter = QSplitter(Qt.Orientation.Horizontal)
#         splitter.addWidget(self.list_widget)
#         splitter.addWidget(right_panel)
        
#         splitter.setStretchFactor(0, 5) 
#         splitter.setStretchFactor(1, 1)

#         layout.addWidget(splitter)

#         main_widget.setLayout(layout)

# class ExperimentWindow(QMainWindow):
#     def __init__(self, name, path):
#         super().__init__()
#         self.name = name
#         self.path = path
#         self.setWindowTitle(f"Space explorer ({name})")
#         main_widget = QWidget()
#         self.setCentralWidget(main_widget)
#         # self.setFixedSize(QSize(400, 150))
#         self.setGeometry(700, 500, 900, 700)
#         self.create_menu()
#         apply_styles(self)

#     def create_menu(self):
#         # Получаем строку меню
#         menu_bar = self.menuBar()

#         # ==== Меню "Файл" ====
#         menu_data = menu_bar.addMenu("Данные")

#         data_action = menu_data.addAction("Датчики")
#         data_action.triggered.connect(self.show_data_window)

#         video_action = menu_data.addAction("Видео")
#         sound_action = menu_data.addAction("Звук")
#         # file_menu = menu_bar.addMenu("Данные")

#         # self.file_submenu = file_menu.addMenu('Тип данных')
#         # button_action = self.file_submenu.addAction("Голова") 
#         # # button_action.triggered.connect(partial(self.change_type, new_type="Голова"))
#         # # button_action = self.file_submenu.addAction("Шея") 
#         # button_action = self.file_submenu.addAction("Грудная клетка")
#         # button_action = self.file_submenu.addAction("Голень") 
#         # button_action = self.file_submenu.addAction("Аудио") 
         
#         # self.file_submenu.triggered.connect(self.on_menu_item_clicked)

#         # # Действие "Открыть"
#         # open_action = file_menu.addAction("Открыть")
#         # open_action.triggered.connect(self.open_file)

#         # # Действие "Сохранить"
#         # save_action = file_menu.addAction("Сохранить")
#         # save_action.triggered.connect(self.save_file)

#         # # Разделитель
#         # file_menu.addSeparator()

#         # # Действие "Выход"
#         # exit_action = file_menu.addAction("Выход")
#         # exit_action.triggered.connect(self.close)

#         # ==== Меню "Помощь" ====
#         help_menu = menu_bar.addMenu("Помощь")

#         # Действие "О программе"
#         about_action = help_menu.addAction("О программе")
#         about_action.triggered.connect(self.about_program)
    

#     def show_data_window(self):
#         self.new_window = ImportDataWindow()
#         self.new_window.show()
    
#     def about_program(self):
#         QMessageBox.about(self, "О программе", "Это простое приложение с меню на PyQt6")