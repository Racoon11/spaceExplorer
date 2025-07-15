from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, 
                             QFileDialog, QComboBox, QHBoxLayout, QListWidget, QMessageBox)
from PyQt5.QtGui import QPixmap
from pandas import read_csv, to_datetime
import pandas as pd
import numpy as np

import os
import shutil
from datetime import datetime

from styles import *
from myjson import *


class ImportDataWindow(QWidget):
    def __init__(self, path, experimentWindow):
        super().__init__()

        self.main_path = path
        self.experimentWindow = experimentWindow
        self.setWindowTitle("Форма ввода данных")
        self.setFixedSize(700, 800)

        # === ЛЕВАЯ ЧАСТЬ: Форма для добавления датчика ===
        left_widget = QWidget()
        left_layout = QVBoxLayout()

        # Имя файла
        self.name_label = QLabel("Имя (укажите, если датчик '-')")
        self.name_edit = QLineEdit()

        # Выбор типа датчика
        self.type_label = QLabel("Выберите датчик:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(['-', 'arduino'] + list(map(str, range(1, 12))))

        # Отображение изображения
        self.image_label = QLabel(self)
        pixmap = QPixmap(':/images/dots2.jpg').scaledToWidth(200)
        self.image_label.setPixmap(pixmap)

        # Путь к файлу
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("Выберите файл...")
        self.browse_button = QPushButton("Обзор")
        self.browse_button.clicked.connect(self.select_file)

        # Кнопка сохранить
        self.save_button = QPushButton("Добавить")
        self.save_button.clicked.connect(self.save_form_data)

        # Компоновка для файла
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_path_edit)
        file_layout.addWidget(self.browse_button)

        # Установка layout для левой части
        left_layout.addWidget(self.image_label)
        left_layout.addWidget(self.name_label)
        left_layout.addWidget(self.name_edit)
        left_layout.addWidget(self.type_label)
        left_layout.addWidget(self.type_combo)
        left_layout.addLayout(file_layout)
        left_layout.addWidget(self.save_button)
        left_widget.setLayout(left_layout)

        # === ПРАВАЯ ЧАСТЬ: Список выбранных файлов ===
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget::item:selected {
                background-color: #d0e7ff;
                color: black;
            }
            QListWidget::item:hover {
                background-color: #f0f0f0;
            }
        """)

        # === ОБЪЕДИНЕНИЕ ЛЕВОЙ И ПРАВОЙ ЧАСТИ ===
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget, stretch=2)   # Левая часть занимает 2/3
        main_layout.addWidget(self.list_widget, stretch=3)  # Правая — 1/3
        
        self.setLayout(main_layout)
        apply_styles(self)
        

    def select_file(self):
        """Открытие диалога выбора файла"""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)   
        file_name, _ = dialog.getOpenFileName(
            self,
            "Выбрать файл",
            "",  # начальный путь (можно оставить пустым)
            "CSV файлы (*.csv);;Текстовые файлы (*.txt)"
        )
        if file_name:
            self.file_path_edit.setText(file_name)

    def save_form_data(self):
        """Сохранение данных формы"""
        selected_type = self.type_combo.currentText()
        file_path = self.file_path_edit.text()
        name = self.name_edit.text()
        if selected_type == '-' and not name:
            return
        if selected_type != '-':
            name = selected_type

        if name == 'arduino' and file_path:
            data = read_csv(file_path)
            try:
                time_series = to_datetime(data.iloc[:,0], format='%H:%M:%S').dt.time
                data = data.iloc[:,1:]
                data['time'] = time_series

                dt1 = datetime.combine(datetime.today(), data['time'][data.shape[0]-1])
                dt2 = datetime.combine(datetime.today(), data['time'][0])
                delta = (dt1 - dt2).total_seconds() * 1000
                mtime = np.linspace(0, delta, data.shape[0])
                data['millisecs'] = mtime

            except Exception as e:
                print(e)
                QMessageBox.critical(
                    self,
                    "Ошибка",
                    "Первый столбец не соответствует формату hh:mm:ss",
                    QMessageBox.StandardButton.Abort
                )
                return
            if 'channels' not in data.columns:
                QMessageBox.critical(
                    self,
                    "Ошибка",
                    "В выбранном файле отсутствует столбец channels",
                    QMessageBox.StandardButton.Abort
                )
                return
            
            for ch in data['channels'].unique():
                data_ch = data[data['channels'] == ch]
                data_ch = data_ch.drop("channels", axis=1)
                self.save_data_from_file(str(ch), selected_type, file_path, data_ch)
            
            self.experimentWindow.create_menu_plot_metrics()
            self.file_path_edit.clear()
            self.type_combo.setCurrentIndex(0)
                
        elif file_path:
            self.save_data_from_file(name, selected_type, file_path)

            self.experimentWindow.create_menu_plot_metrics()
            self.file_path_edit.clear()
            self.type_combo.setCurrentIndex(0)

    def save_data_from_file(self, name, selected_type, path, data=-1):
        item_text = f"[{name}] {path}"
        new_file_path = os.path.join(self.main_path, "data", f"{name}.csv")

        if type(data) == pd.DataFrame:
            data.to_csv(new_file_path, index=False)
        else:
            shutil.copy(path, new_file_path)

        info_file_path = os.path.join(self.main_path, 'info.json')
        experiment_data = load_experiments(info_file_path)
        if not experiment_data:
            experiment_data = {"experiment_data": []}
        print("name:", name, "type", selected_type, "path:", new_file_path)
        experiment_data['experiment_data'].append({"name": name, 'type': selected_type, 'path': new_file_path})
        save_experiments(experiment_data, info_file_path)

        self.add_metrics_to_file(name, new_file_path)
        self.list_widget.addItem(item_text)
            
    def add_metrics_to_file(self, name, path):
        files = load_experiments(os.path.join(self.experimentWindow.path, "info.json"))
        metrics = [] if 'metrics' not in files else files['metrics']
        with open(path) as f:
            cols = f.readline().strip().split(',')
            lines = f.readline().split(',')
        for col, line in zip(cols, lines):
            try:
                float(line)
                for metric in self.experimentWindow.basic_metrics:
                    metrics.append(f"{name}-{col}-{metric}")
            except Exception as e:
                pass
        files['metrics'] = metrics
        save_experiments(files, os.path.join(self.experimentWindow.path, "info.json"))

        

        # Здесь можно добавить логику сохранения данных в файл или базу данных
