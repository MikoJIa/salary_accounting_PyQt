import sqlite3
import sys

from PySide6.QtCore import QDate
from PySide6.QtGui import QImage, QPixmap, Qt
from PySide6.QtWidgets import QApplication,QMessageBox, QWidget, QLabel, QPushButton, QLineEdit, QDateEdit, QTableWidget, QHeaderView , QTableWidgetItem
from style_sheet.styles import title_main, BACKGROUND_DARK_ACCENT, BUTTON_STYLE, DATE_EDIT_COMPACT_STYLE, INPUT_STYLE, TABLE_STYLE
from login_window import LoginWindow
from db_users import DataBase


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
        self.load_table()

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
        self.fio = QLineEdit(self)
        self.fio.move(30, 70)
        self.fio.setPlaceholderText('ФИО')
        self.fio.setStyleSheet(INPUT_STYLE)
        self.fio.setFixedSize(240, 50)

        self.total_hours = QLineEdit(self)
        self.total_hours.move(30, 120)
        self.total_hours.setPlaceholderText("Кол-во часов")
        self.total_hours.setStyleSheet(INPUT_STYLE)
        self.total_hours.setFixedSize(240, 50)

        self.price_one_hour = QLineEdit(self)
        self.price_one_hour.move(30, 170)
        self.price_one_hour.setPlaceholderText("Стоимость часа")
        self.price_one_hour.setStyleSheet(INPUT_STYLE)
        self.price_one_hour.setFixedSize(240, 50)

        self.job_title = QLineEdit(self)
        self.job_title.move(30, 220)
        self.job_title.setPlaceholderText('Должность')
        self.job_title.setStyleSheet(INPUT_STYLE)
        self.job_title.setFixedSize(240, 50)

        self.accrual = QLineEdit(self)
        self.accrual.move(280, 70)
        self.accrual.setPlaceholderText('Начисления')
        self.accrual.setStyleSheet(INPUT_STYLE)
        self.accrual.setFixedSize(240, 50)

        self.vacation_pay = QLineEdit(self)
        self.vacation_pay.move(280, 120)
        self.vacation_pay.setPlaceholderText('Отпускные')
        self.vacation_pay.setStyleSheet(INPUT_STYLE)
        self.vacation_pay.setFixedSize(240, 50)

        self.remains = QLineEdit(self)
        self.remains.move(280, 170)
        self.remains.setPlaceholderText('Остаток')
        self.remains.setStyleSheet(INPUT_STYLE)
        self.remains.setFixedSize(240, 50)

        self.date_edit = QDateEdit(self)
        self.date_edit.setStyleSheet(DATE_EDIT_COMPACT_STYLE)
        self.date_edit.move(30, 270)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("dd.MM.yyyy")
        self.date_edit.setFixedSize(240, 50)

    def input_validity_check(self):
        fio = self.fio.text().strip()
        total_hours = self.total_hours.text().strip().replace(',', '.')
        price_one_hour = self.price_one_hour.text().strip().replace(',', '.')
        job_title = self.job_title.text().strip()
        accrual = self.accrual.text().strip().replace(',', '.')
        vacation_pay = self.vacation_pay.text().strip().replace(',', '.')
        remains = self.remains.text().strip().replace(',', '.')
        date_edit = self.date_edit.text().strip()
        if not fio:
            return None, "Поле ФИО пустое!"
        if len(fio) < 5:
            return None, "Имя и Фамилия должны быть не менее 5 букв!"
        if not job_title:
            return None, "Поле 'Должность' должно быть заполнено!"
        if not total_hours:
            return None, "Поле 'Кол-во часов' не должно быть пустым!"
        try:
            total_hours = float(total_hours)
            price_one_hour = float(price_one_hour)
        except ValueError:
            return None, "Числовые поля должны содержать только числа!"

        data = {
            "fio": fio,
            "total_hours": total_hours,
            "price_one_hour": price_one_hour,
            "job_title": job_title,
            "accrual": accrual,
            "vacation_pay": vacation_pay,
            "remains": remains,
            "record_date": date_edit
        }
        return data, None

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
        self.table.setGeometry(30, 370, 900, 400)
        self.table.setColumnCount(9)
        headers = ['id', 'ФИО', 'Кол-во часов', 'Стоимость часа', 'Должность', 'Начисления', 'Отпускные', 'Остаток', 'Дата']
        self.table.setHorizontalHeaderLabels(headers)
        self.table.resizeColumnsToContents()
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.itemSelectionChanged.connect(self.on_row_selected)

    def get_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        return int(self.table.item(row, 0).text())


    def on_row_selected(self):
        row = self.table.currentRow()
        if row >= 0:
            self.fio.setText(self.table.item(row, 0).text())
            self.total_hours.setText(self.table.item(row, 1).text())
            self.price_one_hour.setText(self.table.item(row, 2).text())
            self.job_title.setText(self.table.item(row, 3).text())
            self.accrual.setText(self.table.item(row, 4).text())
            self.vacation_pay.setText(self.table.item(row, 5).text())
            self.remains.setText(self.table.item(row, 6).text())

    def on_add_record_clicked(self):
        data, error = self.input_validity_check()
        if error:
            QMessageBox.warning(self, "Ошибка вводимых данных", error)
            return
        try:
            conn = sqlite3.connect('salary.db')
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO salary_data (fio, total_hours, price_one_hour, job_title, accrual, vacation_pay, remains, record_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,(
                data['fio'], data['total_hours'], data['price_one_hour'],
                data['job_title'], data['accrual'], data['vacation_pay'],
                data['remains'], data['record_date']
            ))
            conn.commit()
            conn.close()
            self.load_table()
            QMessageBox.information(self, "Успех", "Запись успешно добавлена!")

        except Exception as e:
            QMessageBox.critical(self, str(e), "Запись не добавлена!")

    def on_update_record_clicked(self):
        fio = self.fio.text()
        total_hours = self.total_hours.text()
        price_one_hour = self.price_one_hour.text()
        job_title = self.job_title.text()
        accrual = self.accrual.text()
        vacation_pay = self.vacation_pay.text()
        remains = self.remains.text()
        date_edit = self.date_edit.date().toString("yyyy-MM-dd")
        id = self.get_id()
        try:
            conn = sqlite3.connect('salary.db')
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE salary_date 
            SET fio = ?, total_hours = ?, 
            price_one_hour = ?, job_title = ?, 
            accrual = ?, vacation_pay = ?, remains = ?, 
            record_date = ?
            WHERE id = ? 
            """,
                (fio, total_hours, price_one_hour, job_title, accrual, vacation_pay, remains, date_edit, id)
            )
            conn.commit()
            conn.close()
            return "Запись переписана!"
        except Exception as e:
            return str(e), "Ошибка обновления записи!"

    def on_delete_record_clicked(self, id):
        try:
            conn = sqlite3.connect('salary.dbla')
            cursor = conn.cursor()
            cursor.execute("""
            DELETE FROM salary_date 
            WHERE id = ? 
            """, (id))
            conn.commit()
            conn.close()
            QMessageBox.information("Запись успешно удалена!")
        except Exception as e:
            return str(e), "Ошибка удаления!"

    def get_all_records(self):
        try:
            conn = sqlite3.connect('salary.db')
            cursor = conn.execute("""
            SELECT fio, total_hours, price_one_hour, job_title, accrual, vacation_pay, remains, record_date, id
            FROM salary_data
            ORDER BY record_date DESC
            """)
            rows = cursor.fetchall()
            conn.close()
            return rows
        except Exception as e:
            print(e)
            return []

    def load_table(self):
        col = 0
        new_list_item = {}
        records = self.get_all_records()
        self.table.setRowCount(len(records))
        for row, rec in enumerate(records):
            new_list_item[row] = list(rec)

        for row in range(0, len(new_list_item)):
            sum_hours_price = new_list_item[row][1] * new_list_item[row][2]
            new_list_item[row][6] = sum_hours_price
            col = 0
            for value in new_list_item[row]:
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)
                col += 1
        self.table.setColumnHidden(8, True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    db = DataBase()
    db.init_salary_table()
    #login_window = LoginWindow()
    #if login_window.exec_():
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    #else:
    sys.exit()