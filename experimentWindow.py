from PyQt6.QtWidgets import QMessageBox, QMainWindow
from PyQt6.QtGui import QPixmap, QIcon

import os
import sys

from importDataWindow import *

class ExperimentWindow(QMainWindow):
    def __init__(self, name, path):
        super().__init__()
        self.name = name
        self.path = path
        self.setWindowTitle(f"Space explorer ({name})")
        # self.setFixedSize(QSize(400, 150))
        self.setGeometry(300, 300, 900, 700)
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