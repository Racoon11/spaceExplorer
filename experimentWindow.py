from PyQt5.QtWidgets import (QMessageBox, QMainWindow, QVBoxLayout, QListWidgetItem, 
                             QFrame, QSplitter, QSizePolicy, QGridLayout, 
                             QScrollArea)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize, QTimer

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar

from pandas import read_csv


import random
import os
import sys

from importDataWindow import *
from styles import *
from myjson import *


class ResponsiveTableWidget(QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.min_column_width = 200
        self.min_columns = 3

        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(5, 5, 5, 5)

        self.setStyleSheet("""
            QLabel {
                padding: 8px;
                min-height: 40px;
            }
            QFrame {
                border: 1px solid #ddd;
                margin: 2px;
                background-color: #f9f9f9;
            }
        """)

        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.safe_populate)

        self.populate()

    def safe_populate(self):
        """Только если таймер истёк"""
        if not self.isVisible():
            return
        self.populate()

    def populate(self):
        """Очистка и заполнение таблицы"""
        self.clear_layout(self.layout)

        available_width = self.width()
        max_columns = max(self.min_columns, available_width // self.min_column_width)

        for i, (key, value) in enumerate(self.data):
            row = i // max_columns
            col = i % max_columns

            label = QLabel(f"<b>{key}</b> = {value}")
            label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            frame = QFrame()
            frame_layout = QVBoxLayout(frame)
            frame_layout.addWidget(label)
            frame_layout.setContentsMargins(4, 4, 4, 4)
            frame.setMinimumHeight(50)

            self.layout.addWidget(frame, row, col)

        self.updateGeometry()

    def clear_layout(self, layout):
        """Полное удаление всех виджетов из layout"""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                widget = item.widget()
                layout.removeWidget(widget)
                widget.deleteLater()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_timer.start(200)  # Задержка перед обновлением


class ChartItemWidget(QWidget):
    def __init__(self, title, data, parent=None):
        super().__init__(parent)

        self.title = title
        self.data = data
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Заголовок
        # self.label = QLabel(title)
        # self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # layout.addWidget(self.label)

        # График
        self.figure = Figure(figsize=(5, 2), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.plot()

    def plot(self):
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.plot(self.data, label=self.title)
        # ax.set_title("График")
        ax.set_xlabel("Время")
        ax.legend()
        ax.grid(True)
        self.canvas.draw()
        self.figure.tight_layout()
        self.canvas.updateGeometry()

    # def resizeEvent(self, event):
    #     """Перерисовываем график при изменении размера виджета"""
    #     self.canvas.resize(event.size())
    #     self.canvas.draw()

# Основное окно
class ExperimentWindow(QMainWindow):
    def __init__(self, name, path):
        super().__init__()

        self.name = name
        self.path = path
        self.chosen_plots = []
        self.setWindowTitle(f"Space explorer ({name})")

        # self.setGeometry(200, 200, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        left_panel = QVBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.setMinimumWidth(400)  # Минимальная ширина левой части
        self.list_widget.setStyleSheet("padding: 0; margin: 0;")
        
        left_splitter = QSplitter(Qt.Orientation.Vertical)
        left_splitter.addWidget(self.list_widget)


        data = [
            ("HIC", "1234 м/с²"), ("HIC1", "5678 м/с²"), ("HIC2", "9101 м/с²"),
            ("HIC3", "1121 м/с²"), ("HIC4", "3141 м/с²"), ("HIC5", "5161 м/с²"),
            ("HIC6", "7181 м/с²"), ("HIC7", "9202 м/с²"),
            ("HIC", "1234 м/с²"), ("HIC1", "5678 м/с²"), ("HIC2", "9101 м/с²"),
            ("HIC3", "1121 м/с²"), ("HIC4", "3141 м/с²"), ("HIC5", "5161 м/с²"),
            ("HIC6", "7181 м/с²"), ("HIC7", "9202 м/с²"),
            ("HIC", "1234 м/с²"), ("HIC1", "5678 м/с²"), ("HIC2", "9101 м/с²"),
            ("HIC3", "1121 м/с²"), ("HIC4", "3141 м/с²"), ("HIC5", "5161 м/с²"),
            ("HIC6", "7181 м/с²"), ("HIC7", "9202 м/с²")
        ]

        self.down_panel = ResponsiveTableWidget(data)
        self.down_panel.setStyleSheet("background-color: white;")

        # Оборачиваем её в QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.down_panel)

        self.min_column_width = 200
        # Фиксируем минимальное количество колонок
        self.down_panel.setMinimumWidth(self.min_column_width * 3)

        # Стиль для ScrollArea
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
        """)

        left_splitter.addWidget(scroll_area)
        left_splitter.setStretchFactor(0, 5)
        left_splitter.setStretchFactor(1, 1)

        left_panel.addWidget(self.list_widget)

        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: white;")
        right_panel.setFrameShape(QFrame.Shape.Box)
        right_panel.setLineWidth(1)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_splitter)
        splitter.addWidget(right_panel)

        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter)

        main_widget.setLayout(layout)
        apply_styles(self)
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

        self.menu_plots = menu_bar.addMenu("Графики")
        self.create_menu_plot()
        
        # ==== Меню "Помощь" ====
        help_menu = menu_bar.addMenu("Помощь")

        # Действие "О программе"
        about_action = help_menu.addAction("О программе")
        about_action.triggered.connect(self.about_program)
    
    def create_menu_plot(self):
        files = load_experiments(os.path.join(self.path, "info.json"))
        if not files: return 
        files = files['experiment_data']
        self.menu_plots.clear()
        for fil in files:
            file_menu = self.menu_plots.addMenu(fil['name'])
            with open(fil['path']) as f:
                cols = f.readline().strip().split(',')
            for c in cols:
                col_act = file_menu.addAction(c)
                col_act.setCheckable(True)
                col_act.setChecked(False)
                col_act.triggered.connect(lambda s, c=c, fil=fil: self.show_plot(s, fil, c))
    def show_plot(self, state, info, col):
        if state:
            data = read_csv(info['path'])[col]
            item = QListWidgetItem(self.list_widget)
            widget = ChartItemWidget(f"{info['name']}-{col}", data)
            item.setSizeHint(widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)
            self.chosen_plots.append(f"{info['name']}-{col}")
        else:
            ind = self.chosen_plots.index(f"{info['name']}-{col}")
            item = self.list_widget.takeItem(ind)
            self.list_widget.removeItemWidget(item)
            del item
            self.chosen_plots.pop(ind)

    def show_data_window(self):
        self.new_window = ImportDataWindow(self.path, self)
        self.new_window.show()
    
    def about_program(self):
        QMessageBox.about(self, "О программе", "Это простое приложение с меню на PyQt6")

