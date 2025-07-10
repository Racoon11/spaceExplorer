from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

import sys # Только для доступа к аргументам командной строки

import resources
from mainWindow import *

# app = QApplication(sys.argv)

# # Создаём виджет Qt — окно.
# window = MainWindow()
# window.show()  # Важно: окно по умолчанию скрыто.

# # Запускаем цикл событий.
# app.exec()

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(':/images/spaceship.ico'))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()