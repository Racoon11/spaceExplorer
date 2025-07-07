def apply_styles(widget):
    widget.setStyleSheet("""
        QWidget {
            background-color: #f9f9f9;
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
        }
        
        QLabel {
            color: #333;
            font-weight: bold;
        }
        
        QLineEdit {
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 6px;
            background-color: #fff;
        }
        
        QPushButton {
            background-color: #007acc;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 6px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #005fa3;
        }
        
        QPushButton:pressed {
            background-color: #004a99;
        }
        
        QListWidget {
            outline: 0px; /* Убирает пунктир при фокусе */
        }

        QListWidget::item {
            background-color: #ffffff;
            padding: 2px;
            border-bottom: 1px solid #ddd;
        }

        QListWidget::item:hover {
            background-color: #f0f0f0;
        }

        QListWidget::item:selected {
            background-color: #d0e7ff;
            color: black;
            border-left: 3px solid #0078d7;
        }

        QListWidget::item:pressed {
            background-color: #c0c0c0;
        }
        
        QMenuBar {
            background-color: #007acc;
            color: white;
            border-bottom: 1px solid #005c99;
        }
        
        QMenuBar::item:selected {
            background-color: #004a99;
        }
        
        QMenu {
            background-color: #007acc;
            color: white;
            border: 1px solid #005c99;
        }
        
        QMenu::item:selected {
            background-color: #004a99;
        }
        
        QComboBox {
            border: 1px solid #aaaaaa;
            border-radius: 4px;
            padding: 5px;
            background-color: #ffffff;
            color: #333333;
            min-height: 20px;
            font-size: 14px;
        }

        QComboBox:hover {
            border: 1px solid #888888;
            background-color: #f5f5f5;
        }

        QComboBox::drop-down {
            border: 0px;
            background-color: transparent;
        }
        QComboBox::down-arrow {
            image: url(:/images/down_arrow.png); /* Путь к своей иконке */
            width: 12px;
            height: 12px;
        }

        QComboBox:on {
            border: 1px solid #5555ff;
            background-color: #eef6ff;
        }

        QComboBox:focus {
            border: 1px solid #5555ff;
            outline: 0px;
        }

        QComboBox QAbstractItemView {
            border: 1px solid #cccccc;
            background-color: #ffffff;
            selection-background-color: #d0e7ff;
            selection-color: #000000;
            outline: 0px;
        }
    """)
