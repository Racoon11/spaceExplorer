from PyQt5.QtWidgets import (QVBoxLayout, QFrame, QSizePolicy, QGridLayout, 
                             QWidget, QLabel)
from PyQt5.QtCore import Qt, QTimer

import pyqtgraph as pg

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar

pg.setConfigOption('background', 'white')
pg.setConfigOption('foreground', 'black')

class ResponsiveTableWidget(QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.min_column_width = 150
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

        for i, (key, value) in enumerate(self.data.items()):
            row = i // max_columns
            col = i % max_columns

            label = QLabel(f"<b>{key}</b> = {value}")
            label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            frame = QFrame()
            frame_layout = QVBoxLayout(frame)
            frame_layout.addWidget(label)
            frame_layout.setContentsMargins(4, 4, 4, 4)
            frame.setMinimumHeight(30)

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

def clear_layout(layout):
    if layout is not None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                clear_layout(child.layout())

class ListItemWidget(QWidget):
    def __init__(self, title, data, parent=None):
        super().__init__(parent)
        self.title = title
        self.data = data

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.layout.setSpacing(4)

        # Заголовок
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("""font-weight: bold; font-size: 14px; padding: 5px;
                min-height: 20px;
                max-height: 20px;""")
        self.layout.addWidget(self.title_label)

        # Таблица с данными
        self.table_widget = ResponsiveTableWidget(data)
        self.table_widget.setStyleSheet("background-color: white;")
        self.layout.addWidget(self.table_widget)

        self.setLayout(self.layout)

    def get_data(self):
        return self.data
    
    
    def add_item(self, item, value):
        self.data[item] = value
        clear_layout(self.layout)
        QWidget().setLayout(self.layout)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.layout.setSpacing(4)

        # Заголовок
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet("""font-weight: bold; font-size: 14px; padding: 5px;
                min-height: 20px;
                max-height: 20px;""")
        self.layout.addWidget(self.title_label)

        # Таблица с данными
        self.table_widget = ResponsiveTableWidget(self.data)
        self.table_widget.setStyleSheet("background-color: white;")
        self.setLayout(self.layout) 
        self.update()


# class ChartItemWidget(QWidget):
#     def __init__(self, title, data, parent=None):
#         super().__init__(parent)

#         self.title = title
#         self.data = data
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(0)

#         # Заголовок
#         # self.label = QLabel(title)
#         # self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         # layout.addWidget(self.label)

#         # График
#         self.figure = Figure(figsize=(5, 2), dpi=100)
#         self.canvas = FigureCanvas(self.figure)
#         self.toolbar = NavigationToolbar(self.canvas, self)

#         self.canvas.setSizePolicy(
#             QSizePolicy.Policy.Expanding,
#             QSizePolicy.Policy.Expanding
#         )
#         layout.addWidget(self.toolbar)
#         layout.addWidget(self.canvas)

#         self.plot()

#     def plot(self):
#         ax = self.figure.add_subplot(111)
#         ax.clear()
#         ax.plot(self.data, label=self.title)
#         # ax.set_title("График")
#         ax.set_xlabel("Время")
#         ax.legend(loc="upper right")
#         ax.grid(True)
#         self.canvas.draw()
#         self.figure.tight_layout()
#         self.canvas.updateGeometry()

    # def resizeEvent(self, event):
    #     """Перерисовываем график при изменении размера виджета"""
    #     self.canvas.resize(event.size())
    #     self.canvas.draw()

class ChartItemWidget(QWidget):
    def __init__(self, title, data, parent=None):
        super().__init__(parent)

        self.title = title
        self.data = data

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Заголовок (опционально можно раскомментировать)
        self.label = QLabel(title)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        # График с pyqtgraph
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)

        # Настройки графика
        self.plot_item = self.plot_widget.getPlotItem()
        self.plot_item.setLabel('bottom', 'Время')
        self.plot_item.addLegend()

        self.curve = self.plot_item.plot(
            self.data,
            name=self.title,
            pen = pg.mkPen(color='#007acc', width=2, style=Qt.PenStyle.SolidLine)
        )
        self.setFixedHeight(200) 

        # Сразу строим график
        self.plot()

    def plot(self):
        """Обновляет данные графика"""
        self.curve.setData(self.data)