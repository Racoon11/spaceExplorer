from PyQt5.QtWidgets import QMessageBox, QMainWindow, QVBoxLayout, QListWidgetItem, QFrame, QSplitter, QSizePolicy
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize

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
        self.figure = Figure(figsize=(5, 1.5), dpi=100)
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
        times = list(range(10))
        ax.plot(self.data, label=self.title)
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

        self.down_panel = QFrame()
        self.down_panel.setStyleSheet("background-color: white;")
        self.down_panel.setFrameShape(QFrame.Shape.Box)
        self.down_panel.setLineWidth(1)

        left_splitter.addWidget(self.down_panel)
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
            widget = ChartItemWidget(f'{info['name']}-{col}', data)
            item.setSizeHint(widget.sizeHint() + QSize(0, 50))
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)
            self.chosen_plots.append(f'{info['name']}-{col}')
        else:
            ind = self.chosen_plots.index(f'{info['name']}-{col}')
            item = self.list_widget.takeItem(ind)
            self.list_widget.removeItemWidget(item)
            del item
            self.chosen_plots.pop(ind)

    def show_data_window(self):
        self.new_window = ImportDataWindow(self.path)
        self.new_window.show()
    
    def about_program(self):
        QMessageBox.about(self, "О программе", "Это простое приложение с меню на PyQt6")

