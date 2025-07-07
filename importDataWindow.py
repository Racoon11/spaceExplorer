from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QFileDialog, QComboBox, QHBoxLayout
from PyQt6.QtGui import QPixmap

import os
import sys
import resources

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class ImportDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Форма ввода данных")
        # self.setFixedSize(QSize(400, 150))
        self.setGeometry(300, 300, 400, 300)

        # Тип (выбор из списка)
        self.type_label = QLabel("Выберите датчик:")

        self.image_label = QLabel(self)
        # self.image_label.setGeometry(50, 50, 500, 200)
        pixmap = QPixmap(':/images/dots2.jpg').scaledToWidth(200)

        self.image_label.setPixmap(pixmap)
        

        # self.image_label.setScaledContents(True)
        # self.image_label.resize(300, 200)  # Set desired size

        self.type_combo = QComboBox()
        self.type_combo.addItems(['-'] + list(map(str, range(1, 12))))

        # Путь к файлу
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("Выберите файл...")
        self.browse_button = QPushButton("Обзор")
        self.browse_button.clicked.connect(self.select_file)

        # Кнопка сохранить
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_form_data)

        # Компоновка для файла
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_path_edit)
        file_layout.addWidget(self.browse_button)

         # Основная компоновка
        layout = QVBoxLayout()
        
        layout.addWidget(self.image_label)
        layout.addWidget(self.type_label)
        layout.addWidget(self.type_combo)
        layout.addLayout(file_layout)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def select_file(self):
        """Открытие диалога выбора файла"""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)   
        file_name, _ = dialog.getOpenFileName(self, "Выбрать файл")
        if file_name:
            self.file_path_edit.setText(file_name)

    def save_form_data(self):
        """Сохранение данных формы"""
        selected_type = self.type_combo.currentText()
        file_path = self.file_path_edit.text()

        print("Выбранный тип:", selected_type)
        print("Путь к файлу:", file_path)

        # Здесь можно добавить логику сохранения данных в файл или базу данных
