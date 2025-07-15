import pyqtgraph as pg
from PyQt5 import QtWidgets
import numpy as np
import time


class LivePlotWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live Plot with pyqtgraph")
        self.resize(800, 600)

        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)

        self.plot_line = self.plot_widget.plot(pen='r')

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)  # обновление каждые 50 мс

        self.phase = 0

    def update_plot(self):
        x = np.linspace(0, 10, 1000)
        y = np.sin(x + self.phase)
        self.plot_line.setData(x, y)
        self.phase += 0.1


app = QtWidgets.QApplication([])
window = LivePlotWindow()
window.show()
app.exec()