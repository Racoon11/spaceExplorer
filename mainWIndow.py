from PyQt6.QtWidgets import (QWidget, QPushButton, QMainWindow, QLabel, QVBoxLayout,
                             QTextEdit, QFileDialog, QMessageBox, QHBoxLayout,
                             QListWidget, QListWidgetItem, QFrame
                             )
from PyQt6.QtCore import QSize, Qt


import os
import json

from experimentWindow import *
from styles import *


def load_experiments(FILE_PATH):
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_experiments(experiments, FILE_PATH):
    with open(FILE_PATH, "w") as f:
        json.dump(experiments, f, indent=4)


# Подкласс QMainWindow для настройки главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_type = None

        self.setWindowTitle("Space explorer")
        # self.setMinimumSize(QSize(700, 700)) 
        self.setGeometry(700, 500, 800, 800)

        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        self.create_start_interface()
        # self.create_menu()
    
    def create_start_interface(self):
        window = self
        # Основной layout
        main_layout = QHBoxLayout()

        # === ЛЕВАЯ ЧАСТЬ: Список недавних экспериментов ===
        left_widget = QWidget()
        left_layout = QVBoxLayout()

        recent_experiments_label = QLabel("Недавние эксперименты")
        recent_experiments_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        left_layout.addWidget(recent_experiments_label)

        window.recent_list = QListWidget()

        file_path = "data//experiments.json"
        if os.path.exists(file_path):
            old_experiments = load_experiments(file_path)['experiments']
            experiments = list(filter(lambda exp: os.path.exists(exp['path']), old_experiments))
            save_experiments({"experiments": experiments},  file_path)
            
        else:
            experiments = []

        # Пример данных
        # experiments = [
        #     {"name": "Эксперимент 1", "path": "/home/user/experiments/exp1.json"},
        #     {"name": "Тестовый запуск", "path": "/home/user/experiments/test_run.json"},
        #     {"name": "Проект Альфа", "path": "/home/user/projects/alpha_project.json"}
        # ]

        for exp in experiments:
            item = QListWidgetItem(window.recent_list)
            item.setData(Qt.ItemDataRole.UserRole, {
                "name": exp['name'],
                "path": exp["path"]
            })
            item_widget = QWidget()
            item_layout = QVBoxLayout()
            item_layout.setSpacing(2)

            name_label = QLabel(f"<b>{exp['name']}</b>")
            path_label = QLabel(exp['path'])
            path_label.setStyleSheet("font-size: 10px; color: gray;")

            item_layout.addWidget(name_label)
            item_layout.addWidget(path_label)

            item_widget.setLayout(item_layout)
            item.setSizeHint(item_widget.sizeHint())

            window.recent_list.addItem(item)
            window.recent_list.setItemWidget(item, item_widget)

        left_layout.addWidget(window.recent_list)
        left_widget.setLayout(left_layout)

        # Разделитель между левой и правой частью
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        # === ПРАВАЯ ЧАСТЬ: Кнопки ===
        right_widget = QWidget()
        right_layout = QVBoxLayout()

        new_experiment_button = QPushButton("Создать новый эксперимент")
        open_experiment_button = QPushButton("Открыть существующий")

        # Добавляем отступы сверху для вертикального выравнивания кнопок
        right_layout.addStretch(1)
        right_layout.addWidget(new_experiment_button)
        right_layout.addWidget(open_experiment_button)
        right_layout.addStretch(30)
        

        right_widget.setLayout(right_layout)

        # === Объединение частей ===
        main_layout.addWidget(left_widget, stretch=3)  # 3 части слева
        main_layout.addWidget(separator)
        main_layout.addWidget(right_widget, stretch=1)  # 1 часть справа

         # --- Подключение событий ---
        window.recent_list.itemDoubleClicked.connect(lambda item: self.on_experiment_double_clicked(item))

        # Установка основного layout'а
        container = QWidget()
        container.setLayout(main_layout)

        apply_styles(container)
        window.setCentralWidget(container)

        # Привязка обработчиков (можно добавить позже)
        new_experiment_button.clicked.connect(self.create_experiment_interface)
        open_experiment_button.clicked.connect(lambda: print("Открыть существующий"))
    
    def create_experiment_interface(self):
        """
        Очищает содержимое окна и отображает форму создания эксперимента.
        """

        window = self
        # Очистка центрального виджета
        central_widget = window.centralWidget()
        if central_widget:
            central_widget.setParent(None)

        # Создание нового контейнера
        container = QWidget()
        layout = QVBoxLayout()

        # === Название эксперимента ===
        name_label = QLabel("Название эксперимента:")
        window.experiment_name_input = QLineEdit()
        window.experiment_name_input.setPlaceholderText("Введите название эксперимента")

        # === Путь к папке сохранения ===
        path_layout = QHBoxLayout()
        path_label = QLabel("Путь для сохранения:")

        window.path_display = QLineEdit()
        window.path_display.setReadOnly(True)
        window.path_display.setPlaceholderText("Выберите папку для сохранения")

        select_path_button = QPushButton("Обзор")
        select_path_button.clicked.connect(self.select_save_directory)

        path_layout.addWidget(window.path_display)
        path_layout.addWidget(select_path_button)

        # === Кнопка "Создать" ===
        create_button = QPushButton("Создать")
        create_button.clicked.connect(self.create_experiment)

        # === Добавление элементов в layout ===
        layout.addWidget(name_label)
        layout.addWidget(window.experiment_name_input)
        layout.addWidget(path_label)
        layout.addLayout(path_layout)
        layout.addWidget(create_button)

        # Выравнивание по центру
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(40, 20, 30, 10)
        
        apply_styles(container)

        container.setLayout(layout)
        window.setCentralWidget(container)

    # === Вспомогательные функции ===

    def select_save_directory(window):
        """Открывает диалог выбора директории"""
        directory = QFileDialog.getExistingDirectory(window, "Выберите папку для сохранения")
        if directory:
            window.path_display.setText(directory)


    def create_experiment(window):
        """Обработка нажатия на кнопку 'Создать'"""
        name = window.experiment_name_input.text().strip()
        path = window.path_display.text().strip()

        if not name:
            print("Ошибка: Необходимо указать название эксперимента.")
            return

        if not path:
            print("Ошибка: Необходимо выбрать путь для сохранения.")
            return

        full_path = path

        folder_path = full_path + '/' + name
        os.makedirs(folder_path, exist_ok=True)

        os.makedirs("data", exist_ok=True)
        
        if not os.path.exists("data/experiments.json"):
            with open("data/experiments.json", 'a') as f:
                experiment_data = {'experiments': [{"name": name, "path": folder_path}]}
        else:
            file_path = "data//experiments.json"
            experiment_data = load_experiments(file_path)
            experiments = experiment_data['experiments']
            experiments.append({"name": name, "path": folder_path})
                
        save_experiments(experiment_data, "data/experiments.json")
        window.show_expermient_window(name, path)
        
    def show_expermient_window(self, name, path):
        self.close()
        self.experimentWindow = ExperimentWindow(name, path)
        self.experimentWindow.show()

    def on_experiment_double_clicked(self, item):
        experiment_data = item.data(Qt.ItemDataRole.UserRole)
        if os.path.exists(experiment_data["path"]):
            self.show_expermient_window(experiment_data["name"], experiment_data["path"])
        
        
    def change_type(self, b, new_type):
        self.file_type = new_type
        self.file_submenu 
    def open_file(self):
        #options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", "Текстовые файлы (*.txt);;Все файлы (*)", 
        )
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as f:
                self.text_edit.setText(f.read())

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Сохранить файл", "", "Текстовые файлы (*.txt);;Все файлы (*)"
        )
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(self.text_edit.toPlainText())

    