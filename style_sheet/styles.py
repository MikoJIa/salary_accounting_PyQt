title_main = """
    QLabel {
        background: None;
        color: white;
        padding: 15px 25px;
        font-size: 24px;
        font-weight: bold;
    }
"""

BACKGROUND_DARK_ACCENT = """
    QWidget {
         background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
            stop: 0 #2d2a24,
            stop: 0.5 #3a3530,
            stop: 1 #2a2722);
    }
"""

BUTTON_STYLE = """
    QPushButton {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 #6b5b45,
            stop: 1 #5a4d3a);
        color: #f5f0e6;
        border: none;
        border-radius: 8px;
        font-size: 20px;
        font-weight: bold;
        padding: 8px 16px;
    }
    QPushButton:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 #7d6b52,
            stop: 1 #6b5b45);
    }

    QPushButton:pressed {
        background: #4a3f35;
    }
"""

BALANCE_WITH_ICON = """
    QLabel {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 #6b5b45,
            stop: 1 #5a4d3a);
        color: #f5f0e6;
        border: 2px solid #3498db;
        border-radius: 6px;
        padding: 10px 20px;
        font-size: 20px;
    }
    QLabel:hover {
        background-color: rgba(105, 240, 174, 0.15);
        border-color: #69F0AE;
    }
"""

INPUT_STYLE = """
    QLineEdit {
        color: #FFFFFF;
        font-size: 16px;
        font-family: 'Segoe UI', Arial, sans-serif;
        background-color: #2d2d2d;
        border: 2px solid #3d3d3d;
        border-radius: 8px;
        padding: 10px 15px;
        margin: 5px;
        selection-background-color: #4CAF50;
        selection-color: #FFFFFF;
    }
    QLineEdit:focus {
        border-color: #4CAF50;
        background-color: #333333;
    }
    QLineEdit:hover {
        border-color: #555555;
        background-color: #353535;
    }
    QLineEdit:disabled {
        color: #666666;
        border-color: #2d2d2d;
        background-color: #1a1a1a;
    }
"""

TABLE_STYLE = """
    QTableWidget {
        background-color: #1a1a1a;
        alternate-background-color: #222222;
        border: 2px solid #2d2d2d;
        border-radius: 10px;
        gridline-color: #2d2d2d;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 14px;
        outline: none;
    }
    QTableWidget::item {
        color: #FFFFFF;
        padding: 8px 12px;
        border: none;
    }
    QTableWidget::item:selected {
        background-color: #4CAF50;
        color: #FFFFFF;
    }
    QTableWidget::item:hover {
        background-color: #333333;
    }
    QHeaderView::section {
        background-color: #2d2d2d;
        color: #B0BEC5;
        font-weight: bold;
        font-size: 13px;
        padding: 10px;
        border: none;
        border-right: 1px solid #3d3d3d;
        border-bottom: 2px solid #4CAF50;
    }
    QHeaderView::section:hover {
        background-color: #353535;
    }
    QTableWidget QTableCornerButton::section {
        background-color: #2d2d2d;
        border: none;
    }
"""

# Компактный стиль
DATE_EDIT_COMPACT_STYLE = """
    QDateEdit {
        color: #FFFFFF;
        font-size: 14px;
        font-family: 'Segoe UI', Arial, sans-serif;
        background-color: #2d2d2d;
        border: 1px solid #3d3d3d;
        border-radius: 6px;
        padding: 5px 10px;
        margin: 2px;
    }
    QDateEdit:focus {
        border-color: #4CAF50;
    }
    QDateEdit::drop-down {
        border: none;
        width: 16px;
        subcontrol-origin: padding;
        subcontrol-position: right center;
        margin-right: 3px;
    }
    QDateEdit::down-arrow {
        image: url(images/arrow_down_white.svg);
        width: 10px;
        height: 10px;
    }
"""

STYLE_QDIALOG_WINDOW = """
QDialog {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #1a1a1a,
                                           stop: 1 #0d0d0d);
                border: 2px solid #2d2d2d;
                border-radius: 15px;
            }
            QLabel {
                color: #B0BEC5;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel#title {
                font-size: 28px;
                font-weight: bold;
                color: #4CAF50;
                padding: 20px 0 10px 0;
            }
            QLabel#subtitle {
                font-size: 14px;
                color: #78909C;
                padding: 0 0 20px 0;
            }
            QLabel#error {
                color: #FF5252;
                font-size: 12px;
                padding: 5px;
                background-color: rgba(255, 82, 82, 0.1);
                border-radius: 5px;
            }
            QLineEdit {
                color: #FFFFFF;
                font-size: 14px;
                font-family: 'Segoe UI', Arial, sans-serif;
                background-color: #2d2d2d;
                border: 2px solid #3d3d3d;
                border-radius: 10px;
                padding: 12px 15px;
                margin: 5px 0;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
                background-color: #333333;
            }
            QLineEdit:hover {
                border-color: #555555;
            }
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #4CAF50,
                                           stop: 1 #388E3C);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 14px 30px;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                margin: 10px 0;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #66BB6A,
                                           stop: 1 #43A047);
            }
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #388E3C,
                                           stop: 1 #2E7D32);
            }
            QPushButton#register_btn {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #2196F3,
                                           stop: 1 #1976D2);
            }
            QPushButton#register_btn:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #42A5F5,
                                           stop: 1 #1E88E5);
            }
            QFrame#line {
                background-color: #2d2d2d;
                max-height: 1px;
                margin: 10px 0;
            }
            QProgressBar {
                border: none;
                background-color: #1a1a1a;
                border-radius: 5px;
                max-height: 3px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 5px;
            }
"""

REGISTRATION_WINDOW_STYLE = """
            QDialog {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #1a1a1a,
                                           stop: 1 #0d0d0d);
                border: 2px solid #2d2d2d;
                border-radius: 15px;
            }
            QLabel {
                color: #B0BEC5;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                color: #2196F3;
                padding: 20px 0 10px 0;
            }
            QLabel#subtitle {
                font-size: 14px;
                color: #78909C;
                padding: 0 0 20px 0;
            }
            QLabel#error {
                color: #FF5252;
                font-size: 12px;
                padding: 5px;
                background-color: rgba(255, 82, 82, 0.1);
                border-radius: 5px;
            }
            QLabel#success {
                color: #4CAF50;
                font-size: 12px;
                padding: 5px;
                background-color: rgba(76, 175, 80, 0.1);
                border-radius: 5px;
            }
            QLineEdit {
                color: #FFFFFF;
                font-size: 14px;
                font-family: 'Segoe UI', Arial, sans-serif;
                background-color: #2d2d2d;
                border: 2px solid #3d3d3d;
                border-radius: 10px;
                padding: 12px 15px;
                margin: 5px 0;
            }
            QLineEdit:focus {
                border-color: #2196F3;
                background-color: #333333;
            }
            QLineEdit:hover {
                border-color: #555555;
            }
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #2196F3,
                                           stop: 1 #1976D2);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 14px 30px;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                margin: 10px 0;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #42A5F5,
                                           stop: 1 #1E88E5);
            }
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #1976D2,
                                           stop: 1 #1565C0);
            }
            QPushButton#cancel_btn {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #78909C,
                                           stop: 1 #546E7A);
            }
            QPushButton#cancel_btn:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #90A4AE,
                                           stop: 1 #607D8B);
            }
            QFrame#line {
                background-color: #2d2d2d;
                max-height: 1px;
                margin: 10px 0;
            }
        """