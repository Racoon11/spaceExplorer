from PyQt5.QtWidgets import (QMessageBox, QMainWindow, QVBoxLayout, QListWidgetItem, 
                             QFrame, QSplitter, 
                             QScrollArea)
from PyQt5.QtCore import Qt, QSize

from pandas import read_csv


import random
import os
import sys

from importDataWindow import *
from styles import *
from myjson import *
from specialWidgets import *


# Основное окно
class ExperimentWindow(QMainWindow):
    def __init__(self, name, path):
        super().__init__()

        self.name = name
        self.path = path
        self.info_file_path = os.path.join(self.path, "info.json")
        self.chosen_plots = []
        self.chosen_metrics = []
        self.possible_metrics = {"max": max, "min": min, "mean": lambda x: round(sum(x)/len(x), 4)}
        self.basic_metrics = ['max', 'min', 'mean']
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


        self.down_panel = QListWidget()

        self.down_panel.setStyleSheet("""
            QListWidget {
                border: none;
                background-color: #f0f0f0;
                padding: 0px;
            }
            QListWidget::item {
                border: 1px solid #cccccc;
                margin: 2px;
                padding: 0px;
                background-color: white;
                border-radius: 4px;
            }
        """)
        self.down_panel_widgets = {}
        special_list_item = self.add_down_item("Метрики безопасности", {})
        self.down_panel_widgets['special'] = special_list_item

        # self.add_down_item("title", data)
        # self.add_down_item("title", data)

        # self.down_panel = ResponsiveTableWidget(data)
        # self.down_panel.setStyleSheet("background-color: white;")

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
    
    def add_down_item(self, title, data, row=-1):
        item = QListWidgetItem()
    
        widget = ListItemWidget(title, data)
        
        # Устанавливаем размер элемента под содержимое
        widget_size = widget.sizeHint()
        item.setSizeHint(widget_size)

        if row != -1:
            self.down_panel.insertItem(row, item)
        else:
            self.down_panel.addItem(item)
        self.down_panel.setItemWidget(item, widget)

        return item
    
    
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
        
        self.menu_metrics = menu_bar.addMenu("Метрики")
        self.create_menu_plot_metrics()
        
        # ==== Меню "Помощь" ====
        help_menu = menu_bar.addMenu("Помощь")

        # Действие "О программе"
        about_action = help_menu.addAction("О программе")
        about_action.triggered.connect(self.about_program)
    
    
    def create_menu_plot_metrics(self):
        files = load_experiments(os.path.join(self.path, "info.json"))
        if not files: return 
        plots = [] if 'plots' not in files else files['plots']
        metrics = [] if 'metrics' not in files else files['metrics']
        files = files['experiment_data']

        self.menu_plots.clear()
        self.menu_metrics.clear()
        for fil in files:
            file_menu = self.menu_plots.addMenu(fil['name'])
            file_metric_menu = self.menu_metrics.addMenu(fil['name'])
            with open(fil['path']) as f:
                cols = f.readline().strip().split(',')
                lines = f.readline().split(',')
            for c, line in zip(cols, lines):
                try:
                    float(line)
                except Exception as e:
                    print(e)
                    continue
                col_act = file_menu.addAction(c)
                col_act.setCheckable(True)
                if f"{fil['name']}-{c}" in plots:
                    col_act.setChecked(True)
                    self.show_plot(True, fil, c)
                else:
                    col_act.setChecked(False)
                col_act.triggered.connect(lambda s, c=c, fil=fil: self.show_plot(s, fil, c))

                col_metric_menu = file_metric_menu.addMenu(c)
                for metric in self.possible_metrics:
                    met_act = col_metric_menu.addAction(metric)
                    met_act.triggered.connect(lambda s, fil=fil, c=c, metric_name=metric, metric_function=self.possible_metrics[metric]: 
                                              self.add_metric_to_panel(s, fil, c, metric_name, metric_function))
                    met_act.setCheckable(True)
                    if f"{fil['name']}-{c}-{metric}" in metrics:
                        met_act.setChecked(True)
                        self.add_metric_to_panel(True, fil, c, metric, self.possible_metrics[metric])
                    else:
                        met_act.setChecked(False)
                    
    def add_metric_to_panel(self, state, fil, c, metric_name, metric_function):
               
        if state:
            if fil['name'] not in self.down_panel_widgets:
                self.down_panel_widgets[fil['name']] = self.add_down_item(fil['name'], {})
            
            # Get current widget
            cur_widget = self.down_panel.itemWidget(self.down_panel_widgets[fil['name']])
            data = cur_widget.data.copy()

            # delete widget and list item
            row = self.down_panel.row(self.down_panel_widgets[fil['name']]) # get the index of the element
            cur_widget.deleteLater()
            self.down_panel.takeItem(row)

            # update data and create new list item
            data[f"{c}_{metric_name}"] = metric_function(self.get_data(fil['path'], c))
            self.down_panel_widgets[fil['name']] = self.add_down_item(fil['name'], data, row)
            self.chosen_metrics.append(f"{fil['name']}-{c}-{metric_name}")
        
        else:
            # Get current widget
            cur_widget = self.down_panel.itemWidget(self.down_panel_widgets[fil['name']])
            data = cur_widget.data.copy()
            self.chosen_metrics.remove(f"{fil['name']}-{c}-{metric_name}")

            # delete widget and list item
            row = self.down_panel.row(self.down_panel_widgets[fil['name']])
            cur_widget.deleteLater()
            self.down_panel.takeItem(row)

            # update data and create new list item
            if f"{c}_{metric_name}" in data:
                del data[f"{c}_{metric_name}"]
            if data:
                self.down_panel_widgets[fil['name']] = self.add_down_item(fil['name'], data, row)
            

    def get_data(self, path, col):
        data = read_csv(path)[col]
        return data.to_numpy()

    def show_plot(self, state, info, col):
        if state:
            data = self.get_data(info['path'], col)
            item = QListWidgetItem(self.list_widget)
            widget = ChartItemWidget(f"{info['name']}-{col}", data)
            item.setSizeHint(QSize(widget.width(), 200)) 
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
    

    def save_data(self):
        """Сохранение данных, например, в JSON-файл"""
        data_to_save = load_experiments(os.path.join(self.path, "info.json"))
        data_to_save['plots'] = self.chosen_plots
        data_to_save['metrics'] = self.chosen_metrics
        save_experiments(data_to_save, os.path.join(self.path, "info.json"))

    def closeEvent(self, event):
        """
        Сохранение данных перед закрытием окна
        """
        reply = QMessageBox.question(
            self,
            'Выход',
            "Вы хотите сохранить данные перед выходом?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No |
            QMessageBox.StandardButton.Cancel
        )

        if reply == QMessageBox.StandardButton.Cancel:
            event.ignore()  # Отмена закрытия
        else:
            if reply == QMessageBox.StandardButton.Yes:
                self.save_data()

            event.accept()  # Разрешаем закрытие окна

