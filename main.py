import sys

from PySide6.QtCore import QDate
from PySide6.QtGui import QImage, QPixmap, Qt
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QDateEdit, QTableWidget
from style_sheet.styles import title_main, BACKGROUND_DARK_ACCENT, BUTTON_STYLE, DATE_EDIT_COMPACT_STYLE, INPUT_STYLE, TABLE_STYLE
from login_window import LoginWindow


class MainWindow(QWidget):
    accrual = 0
    balance = 0

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setGeometry(400, 200, 800, 750)
        self.setWindowTitle('Main Window accounting')
        self.setUpMainWindow()
        self.show()


    def setUpMainWindow(self):
        self.setStyleSheet(BACKGROUND_DARK_ACCENT)
        self.header_section()
        self.create_input_field()
        self.button_section()
        self.table_section()

    def header_section(self):
        # Создаём заголовок
        self.title_label = QLabel('Программа для учёта зарплат', self)
        self.title_label.move(190, 0)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.title_label.setStyleSheet(title_main)

        # Создаём иконку для заголовка
        image_source = 'images/home_24dp_FFFFFF_FILL0_wght400_GRAD0_opsz24.svg'
        icon_size = 33
        img_label = QLabel(self)
        img_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        img_label.move(180, 20)
        img_pixmap = QPixmap(image_source)
        scaled_pixmap = img_pixmap.scaled(
            icon_size, icon_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        img_label.setPixmap(scaled_pixmap)

    def create_input_field(self):
        self.input_for_fio = QLineEdit(self)
        self.input_for_fio.move(30, 70)
        self.input_for_fio.setPlaceholderText('ФИО')
        self.input_for_fio.setStyleSheet(INPUT_STYLE)
        self.input_for_fio.setFixedSize(240, 50)

        self.input_for_total_hours = QLineEdit(self)
        self.input_for_total_hours.move(30, 120)
        self.input_for_total_hours.setPlaceholderText("Кол-во часов")
        self.input_for_total_hours.setStyleSheet(INPUT_STYLE)
        self.input_for_total_hours.setFixedSize(240, 50)

        self.input_for_price_one_hour = QLineEdit(self)
        self.input_for_price_one_hour.move(30, 170)
        self.input_for_price_one_hour.setPlaceholderText("Стоимость часа")
        self.input_for_price_one_hour.setStyleSheet(INPUT_STYLE)
        self.input_for_price_one_hour.setFixedSize(240, 50)

        self.input_for_job_title = QLineEdit(self)
        self.input_for_job_title.move(30, 220)
        self.input_for_job_title.setPlaceholderText('Должность')
        self.input_for_job_title.setStyleSheet(INPUT_STYLE)
        self.input_for_job_title.setFixedSize(240, 50)

        self.date_edit = QDateEdit(self)
        self.date_edit.setStyleSheet(DATE_EDIT_COMPACT_STYLE)
        self.date_edit.move(30, 270)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("dd.MM.yyyy")
        self.date_edit.setFixedSize(240, 50)

    def button_section(self):
        self.button_add_record = QPushButton("Добавить запись", self)
        self.button_add_record.move(550, 70)
        self.button_add_record.setStyleSheet(BUTTON_STYLE)
        self.button_add_record.clicked.connect(self.on_add_record_clicked)

        self.button_update_record = QPushButton("Изменить запись", self)
        self.button_update_record.move(550, 120)
        self.button_update_record.setStyleSheet(BUTTON_STYLE)
        self.button_update_record.clicked.connect(self.on_update_record_clicked)

        self.button_delete_record = QPushButton("Удалить запись", self)
        self.button_delete_record.move(550, 170)
        self.button_delete_record.setStyleSheet(BUTTON_STYLE)
        self.button_delete_record.clicked.connect(self.on_delete_record_clicked)
        self.button_delete_record.setFixedSize(200, 45)

    def table_section(self):
        self.table = QTableWidget(self)
        self.table.setStyleSheet(TABLE_STYLE)
        self.table.setGeometry(30, 340, 740, 400)
        self.table.setColumnCount(7)
        headers = ['ФИО', 'Кол-во часов', 'Стоимость часа', 'Должность', 'Начисления', 'Отпускные', 'Дата']
        self.table.setHorizontalHeaderLabels(headers)
        self.table.resizeColumnsToContents()


    def on_add_record_clicked(self):
        pass

    def on_update_record_clicked(self):
        pass

    def on_delete_record_clicked(self):
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    #login_window = LoginWindow()
    #if login_window.exec_():
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    #else:
    sys.exit()