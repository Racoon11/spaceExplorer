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
    """)
