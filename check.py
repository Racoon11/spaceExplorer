import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class InteractivePlot(QWidget):
    def __init__(self, parent=None):
        super(InteractivePlot, self).__init__(parent)

        # Создаем фигуру и оси
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Добавляем на график
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.plot()

    def plot(self):
        ax = self.figure.add_subplot(111)
        ax.clear()
        x = [0, 1, 2, 3, 4, 5]
        y = [x_i**2 for x_i in x]
        ax.plot(x, y, label="y = x²")
        ax.set_title("Интерактивный график")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.legend()
        ax.grid(True)
        self.canvas.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Интерактивный график в PyQt5")
        self.setGeometry(100, 100, 800, 600)

        # Основной виджет
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)

        # Добавляем график
        self.plot_widget = InteractivePlot()
        layout.addWidget(self.plot_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())