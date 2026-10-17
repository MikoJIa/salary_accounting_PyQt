import sqlite3
import sys

from PySide6.QtCore import QDate
from PySide6.QtGui import QImage, QPixmap, Qt
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QCheckBox,
                               QVBoxLayout, QGridLayout, QMessageBox,
                               QMainWindow, QWidget, QLabel,
                               QPushButton, QLineEdit, QDateEdit,
                               QTableWidget, QHeaderView , QTableWidgetItem)
from style_sheet.styles import (title_main, BACKGROUND_DARK_ACCENT, BUTTON_STYLE,
                                DATE_EDIT_COMPACT_STYLE, INPUT_STYLE, TABLE_STYLE,
                                QMessage_style, QCHECK_BOX_DATE, RESET_LABEL)
from login_window import LoginWindow
from db_users import DataBase


class MainWindow(QMainWindow):
    accrual = 0
    balance = 0

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setGeometry(400, 200, 1150, 750)
        self.setWindowTitle('Main Window accounting')
        self.setUpMainWindow()
        self.show()


    def setUpMainWindow(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)
        central.setStyleSheet(BACKGROUND_DARK_ACCENT)
        header_con = QWidget()
        self.header_section(header_con)
        main_layout.addWidget(header_con, stretch=0)
        top_row = QHBoxLayout()
        form_container = QWidget()
        self.create_input_field(form_container)
        top_row.addWidget(form_container, stretch=1)
        buttons_container = QWidget()
        self.button_section(buttons_container)
        top_row.addWidget(buttons_container, stretch=0)
        main_layout.addLayout(top_row, stretch=0)
        table_container = QWidget()
        self.table_section(table_container)
        main_layout.addWidget(table_container, stretch=1)
        search_container = QWidget()
        self.create_search_section(search_container)
        main_layout.addWidget(search_container, stretch=0)
        self.load_table()

    def header_section(self, container):
        # Создаём заголовок
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # Создаём иконку для заголовка
        image_source = 'images/home_24dp_FFFFFF_FILL0_wght400_GRAD0_opsz24.svg'
        icon_size = 33
        self.img_label = QLabel()
        self.img_pixmap = QPixmap(image_source)
        scaled_pixmap = self.img_pixmap.scaled(
            icon_size, icon_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.img_label.setPixmap(scaled_pixmap)

        self.title_label = QLabel('Программа для учёта зарплат')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.title_label.setStyleSheet(title_main)

        layout.addStretch(1)
        layout.addWidget(self.img_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addStretch(1)

        return layout

    def create_input_field(self, container):
        grid = QGridLayout(container)
        grid.setContentsMargins(30, 30, 30, 30)
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(10)

        self.fio = QLineEdit(self)
        self.fio.setPlaceholderText('ФИО')
        self.fio.setStyleSheet(INPUT_STYLE)
        self.fio.setMinimumHeight(40)

        self.total_hours = QLineEdit(self)
        self.total_hours.setPlaceholderText("Кол-во часов")
        self.total_hours.setStyleSheet(INPUT_STYLE)
        self.total_hours.setMinimumHeight(40)

        self.price_one_hour = QLineEdit(self)
        self.price_one_hour.setPlaceholderText("Стоимость часа")
        self.price_one_hour.setStyleSheet(INPUT_STYLE)
        self.price_one_hour.setMinimumHeight(40)

        self.job_title = QLineEdit(self)

        self.job_title.setPlaceholderText('Должность')
        self.job_title.setStyleSheet(INPUT_STYLE)
        self.job_title.setMinimumHeight(40)

        self.accrual = QLineEdit(self)
        self.accrual.setPlaceholderText('Начисления')
        self.accrual.setStyleSheet(INPUT_STYLE)
        self.accrual.setMinimumHeight(40)

        self.vacation_pay = QLineEdit(self)
        self.vacation_pay.setPlaceholderText('Отпускные')
        self.vacation_pay.setStyleSheet(INPUT_STYLE)
        self.vacation_pay.setMinimumHeight(40)

        self.remains = QLineEdit(self)
        self.remains.setPlaceholderText('Остаток')
        self.remains.setStyleSheet(INPUT_STYLE)
        self.remains.setMinimumHeight(40)

        self.employee_id = QLineEdit(self)
        self.employee_id.setPlaceholderText('Номер работника')
        self.employee_id.setStyleSheet(INPUT_STYLE)
        self.employee_id.setMinimumHeight(40)

        self.date_edit = QDateEdit(self)
        self.date_edit.setStyleSheet(DATE_EDIT_COMPACT_STYLE)
        self.date_edit.move(30, 270)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("dd.MM.yyyy")
        self.date_edit.setMinimumHeight(40)

        grid.addWidget(self.fio, 0, 0)
        grid.addWidget(self.total_hours, 1, 0)
        grid.addWidget(self.price_one_hour, 2, 0)
        grid.addWidget(self.job_title, 3, 0)
        grid.addWidget(self.date_edit, 4, 0)

        grid.addWidget(self.accrual, 0, 1)
        grid.addWidget(self.vacation_pay, 1, 1)
        grid.addWidget(self.remains, 3, 1)
        grid.addWidget(self.employee_id, 2, 1)

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        return grid

    def input_validity_check(self):
        fio = self.fio.text().strip()
        total_hours = self.total_hours.text().strip().replace(',', '.')
        price_one_hour = self.price_one_hour.text().strip().replace(',', '.')
        job_title = self.job_title.text().strip()
        accrual = self.accrual.text().strip().replace(',', '.')
        vacation_pay = self.vacation_pay.text().strip().replace(',', '.')
        employee_id = self.employee_id.text().strip()
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
            accrual = float(accrual) if accrual else 0.0
            vacation_pay = float(vacation_pay) if vacation_pay else 0.0
        except ValueError:
            return None, "Числовые поля должны содержать только числа!"

        remains = total_hours * price_one_hour - accrual - vacation_pay

        data = {
            "fio": fio,
            "total_hours": total_hours,
            "price_one_hour": price_one_hour,
            "job_title": job_title,
            "accrual": accrual,
            "vacation_pay": vacation_pay,
            "remains": remains,
            "employee_id": employee_id,
            "record_date": date_edit
        }
        return data, None

    def button_section(self, container):
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.button_add_record = QPushButton("Добавить запись", self)
        self.button_add_record.setStyleSheet(BUTTON_STYLE)
        self.button_add_record.clicked.connect(self.on_add_record_clicked)

        self.button_update_record = QPushButton("Изменить запись", self)
        self.button_update_record.setStyleSheet(BUTTON_STYLE)
        self.button_update_record.clicked.connect(self.on_update_record_clicked)

        self.button_delete_record = QPushButton("Удалить запись", self)
        self.button_delete_record.setStyleSheet(BUTTON_STYLE)
        self.button_delete_record.clicked.connect(self.on_delete_record_clicked)

        layout.addWidget(self.button_add_record)
        layout.addWidget(self.button_update_record)
        layout.addWidget(self.button_delete_record)
        return layout


    def table_section(self, contains):
        layout = QVBoxLayout(contains)
        layout.setContentsMargins(0, 0, 0, 0)
        self.table = QTableWidget(self)
        self.table.setStyleSheet(TABLE_STYLE)
        self.table.setColumnCount(10)
        headers = ['ФИО', 'Кол-во часов', 'Стоимость часа', 'Должность', 'Начисления', 'Отпускные', 'Остаток', 'Дата', 'Номер раб-к', 'id']
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.itemSelectionChanged.connect(self.on_row_selected)
        layout.addWidget(self.table)

    def get_emp_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None

        return int(self.table.item(row, 8).text())

    def get_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 9)
        if item is None:
            return None
        return int(item.text()) if item else None

    def create_search_section(self, container):
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 5, 0, 5)
        layout.setSpacing(10)

        self.search_input_fio = QLineEdit()
        self.search_input_fio.setPlaceholderText("Поиск по ФИО")
        self.search_input_fio.setStyleSheet(INPUT_STYLE)
        self.search_input_fio.setMinimumHeight(40)
        self.search_input_fio.returnPressed.connect(self.performs_search)
        layout.addWidget(self.search_input_fio, stretch=3)


        self.checkbox_date = QCheckBox("По дате", self)
        #self.checkbox_date.setStyleSheet(QCHECK_BOX_DATE)
        self.checkbox_date.setMinimumHeight(40)
        self.checkbox_date.stateChanged.connect(self.checkbox_changed)
        layout.addWidget(self.checkbox_date, stretch=0)

        self.search_input_date = QDateEdit()
        self.search_input_date.setStyleSheet(DATE_EDIT_COMPACT_STYLE)
        self.search_input_date.setDate(QDate.currentDate())
        self.search_input_date.setDisplayFormat("dd.MM.yyyy")
        self.search_input_date.setMinimumHeight(40)
        self.search_input_date.setEnabled(False)
        self.search_input_date.dateChanged.connect(self.checkbox_changed)
        layout.addWidget(self.search_input_date, stretch=2)

        self.search_button = QPushButton("Найти")
        self.search_button.setStyleSheet(BUTTON_STYLE)
        self.search_button.setMinimumHeight(40)
        self.search_button.setMinimumWidth(120)
        self.search_button.clicked.connect(self.performs_search)
        layout.addWidget(self.search_button, stretch=0)

        self.reset_button = QPushButton("Сбросить")
        self.reset_button.setStyleSheet(BUTTON_STYLE)
        self.reset_button.setMinimumHeight(40)
        self.reset_button.setMinimumWidth(120)
        self.reset_button.clicked.connect(self.search_reset)
        layout.addWidget(self.reset_button, stretch=0)

        self.search_info = QLabel("0")
        self.setStyleSheet(RESET_LABEL)
        self.search_info.setMinimumWidth(100)
        self.search_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.search_info, stretch=0)

    def query_search_changed(self, fio=None, date=None):
        try:
            conn = sqlite3.connect("salary.db")
            cursor = conn.cursor()
            request = """
            SELECT fio, total_hours, price_one_hour,
            job_title, accrual, vacation_pay, remains, record_date, employee_id, id
            FROM salary_data
            WHERE 1=1
            """
            lst_params = []

            if fio:
                request += " AND LOWER(fio) LIKE LOWER(?)"
                lst_params.append(f"%{fio}%")
            if date:
                request += " AND record_date = ?"
                lst_params.append(date)
            request += " ORDER BY record_date DESC"
            print(f"SQL: {request}")  # ← ОТЛАДКА
            print(f"PARAMS: {lst_params}")
            cursor.execute(request, lst_params)
            row = cursor.fetchall()
            conn.close()
            print(f"РЕЗУЛЬТАТ: {len(row)} записей")  # ← ОТЛАДКА
            return row
        except Exception as e:
            print(e)
            return f"Ошибка - {e}", []

    def checkbox_changed(self):
        self.search_input_date.setEnabled(self.checkbox_date.isChecked())

    def performs_search(self):
        fio = self.search_input_fio.text().strip()
        date = None
        if self.checkbox_date.isChecked():
            date = self.search_input_date.date().toString("dd.MM.yyyy")
        if not fio and not date:
            self.load_table()
            self.search_info.setText("0")
            return
        record = self.query_search_changed(fio=fio if fio else None, date=date)
        self.display(record)
        self.search_info.setText(f"Найдено: {len(record)}")

    def search_reset(self):
        self.search_input_date.setDate(QDate.currentDate())
        self.search_input_fio.clear()
        self.checkbox_date.setChecked(False)
        self.search_info.setText("0")
        self.load_table()

    def all_row_clear(self):
        self.fio.clear()
        self.total_hours.clear()
        self.price_one_hour.clear()
        self.job_title.clear()
        self.accrual.clear()
        self.vacation_pay.clear()
        self.employee_id.clear()
        self.remains.clear()
        self.date_edit.setDate(QDate.currentDate())


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
            self.employee_id.setText(self.table.item(row, 8).text())

    def on_add_record_clicked(self):
        data, error = self.input_validity_check()
        if error:
            QMessageBox.warning(self, "Ошибка вводимых данных", error)
            return
        try:
            conn = sqlite3.connect('salary.db')
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO salary_data (employee_id, fio, total_hours, price_one_hour, job_title, accrual, vacation_pay, remains, record_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,(
                data['employee_id'], data['fio'], data['total_hours'], data['price_one_hour'],
                data['job_title'], data['accrual'], data['vacation_pay'],
                data['remains'], data['record_date']
            ))
            conn.commit()
            conn.close()
            self.load_table()
            self.all_row_clear()
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
        date_edit = self.date_edit.date().toString("dd.MM.yyyy")
        emp_id = self.get_emp_id()
        if emp_id is None:
            QMessageBox.warning(self, "Ошибка", "Необходимо выбрать запись!")
            return
        answer = QMessageBox.question(self, "Необходимо ваше подтверждение!",
                                      f"Вы точно хотите изменить данные?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if answer != QMessageBox.StandardButton.Yes:
            return
        if float(remains) != 0:
            remains = float(remains)
            accrual = float(accrual) if accrual else 0.0
            vacation_pay = float(vacation_pay) if vacation_pay else 0.0
            remains = remains - accrual - vacation_pay

        try:
            conn = sqlite3.connect('salary.db')
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO salary_data 
            (employee_id, fio, total_hours, 
            price_one_hour, job_title, 
            accrual, vacation_pay, remains, 
            record_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) 
            """,
                (emp_id, fio, total_hours, price_one_hour,
                 job_title, accrual,
                 vacation_pay, remains,
                 date_edit)
            )
            conn.commit()
            conn.close()
            self.load_table()
            self.all_row_clear()
            QMessageBox.information(self, "Успешно!", "Запись изменена!")
        except Exception as e:
            QMessageBox.warning(self, str(e), "Ошибка обновления записи!")

    def on_delete_record_clicked(self):
        rec_id = self.get_id()
        if rec_id is None:
            QMessageBox.warning(self, "Внимание", "Необходимо выбрать запись для удаления!")
            return
        answer = QMessageBox.question(self, "Необходимо ваше подтверждение!",
                                      f"Вы желаете удалить выбранную запись?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if answer != QMessageBox.StandardButton.Yes:
            return
        try:
            conn = sqlite3.connect('salary.db')
            cursor = conn.cursor()
            cursor.execute("""
            DELETE FROM salary_data
            WHERE id = ? 
            """, (rec_id,))
            if cursor.rowcount == 0:
                QMessageBox.warning(self, "Ошибка!", "Таких данных нет!")
                return
            conn.commit()
            conn.close()
            self.load_table()
            QMessageBox.information(self, "Успех!", "Запись успешно удалена!")
        except Exception as e:
            QMessageBox.critical(self, str(e), "Ошибка удаления!")
            return

    def get_all_records(self):
        try:
            conn = sqlite3.connect('salary.db')
            cursor = conn.execute("""
            SELECT fio, total_hours, price_one_hour, job_title, accrual, vacation_pay, remains, record_date, employee_id, id
            FROM salary_data
            ORDER BY record_date DESC
            """)
            rows = cursor.fetchall()
            conn.close()
            return rows

        except Exception as e:
            print(e)
            return []

    def display(self, record):
        self.table.setRowCount(0)
        self.table.setRowCount(len(record))
        for row, rec in enumerate(record):
            for col, value in enumerate(rec):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)
        self.table.viewport().update()
        self.table.setColumnHidden(9, True)

    def load_table(self):
        record = self.get_all_records()
        self.display(record)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(QMessage_style)
    db = DataBase()
    db.init_salary_table()
    #login_window = LoginWindow()
    #if login_window.exec_():
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    #else:
    sys.exit()