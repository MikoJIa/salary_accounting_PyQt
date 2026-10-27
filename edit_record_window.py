import sqlite3

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QDateEdit, QPushButton, QLabel,
    QMessageBox, QDialogButtonBox
)
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QDoubleValidator
from style_sheet.styles import (
    STYLE_QDIALOG_WINDOW, INPUT_STYLE,
    DATE_EDIT_COMPACT_STYLE, BUTTON_STYLE
)


class EditRecordWindow(QDialog):

    def __init__(self, db, rec_id, parent=None):
        super().__init__(parent)
        self.db = db
        self.rec_id = rec_id
        self.lst_data = []

        self.setWindowTitle("Изменение записи")
        self.setModal(True)
        self.setFixedSize(500, 650)
        self.setStyleSheet(STYLE_QDIALOG_WINDOW)
        self.setup_ui()
        self.load_record()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(15)

        title = QLabel("Изменение записи")
        title.setObjectName("title_label")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(12)

        self.job_input = QLineEdit()
        self.job_input.setStyleSheet(INPUT_STYLE)
        self.job_input.setPlaceholderText("Программист")
        form.addRow("Должность:", self.job_input)

        self.date_input = QDateEdit()
        self.date_input.setStyleSheet(DATE_EDIT_COMPACT_STYLE)
        self.date_input.setDisplayFormat("dd.MM.yyyy")
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        form.addRow("Дата:", self.date_input)

        self.accrual_input = QLineEdit()
        self.accrual_input.setStyleSheet(INPUT_STYLE)
        self.accrual_input.setPlaceholderText("1000")
        self.accrual_input.setValidator(QDoubleValidator(0, 100000, 2))
        form.addRow("Начисления:", self.accrual_input)

        self.vacation_pay_input = QLineEdit()
        self.vacation_pay_input.setStyleSheet(INPUT_STYLE)
        self.vacation_pay_input.setPlaceholderText("1000")
        self.vacation_pay_input.setValidator(QDoubleValidator(0, 10000, 2))
        form.addRow("Отпускные:", self.vacation_pay_input)

        self.remains_input = QLineEdit()
        self.remains_input.setStyleSheet(INPUT_STYLE)
        self.remains_input.setPlaceholderText("5000")
        self.remains_input.setValidator(QDoubleValidator(0, 10000, 2))
        form.addRow("Остаток:", self.remains_input)
        layout.addLayout(form)

        buttons = QHBoxLayout()
        buttons.setSpacing(10)

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.setStyleSheet(BUTTON_STYLE)
        self.save_btn.setMinimumHeight(40)
        self.save_btn.clicked.connect(self.on_save)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setStyleSheet(BUTTON_STYLE)
        self.cancel_btn.setMinimumHeight(40)
        self.cancel_btn.clicked.connect(self.reject)

        buttons.addWidget(self.save_btn)
        buttons.addWidget(self.cancel_btn)
        layout.addLayout(buttons)

        #self.hours_input.textChanged.connect(self.update_remains)
        #self.price_input.textChanged.connect(self.update_remains)

    def load_record(self):
        conn = sqlite3.connect("salary.db")
        cursor = conn.cursor()
        cursor.execute("""
        SELECT employee_id, fio, total_hours, 
            price_one_hour, job_title, 
            accrual, vacation_pay, remains, 
            record_date
        FROM salary_data
        WHERE id = ?
        """, (self.rec_id, ))
        row = cursor.fetchone()
        conn.close()
        if not row:
            QMessageBox.warning(self, "Ошибка", "Запись не найдена!")
            self.reject()
            return
        employee_id, fio, hours, price, job, accrual, vacation_pay, remains, date_str = row

        for item in row:
            self.lst_data.append(item)
        #self.hours_input.setText(str(hours or 0))
        #self.price_input.setText(str(price or 0))
        self.job_input.setText(job or "")
        self.vacation_pay_input.setText(str(vacation_pay or 0))
        self.accrual_input.setText(str(accrual or 0))
        self.remains_input.setText(str(remains or 0))
        date = QDate.fromString(date_str, "dd.MM.yyyy")
        if not date.isValid():
            date = QDate.fromString(date_str, "yyyy-MM-dd")
        if date.isValid():
            self.date_input.setDate(date)

        self.update_remains()
        return self.lst_data

    def update_remains(self):
        try:
            accrual = float(self.accrual_input.text().replace(',', '.') or 0)
            vacation_pay = float(self.vacation_pay_input.text().replace(',', '.') or 0)
            remains = float(self.remains_input.text().replace(',', '.'))
            if remains != 0:
                self.remains_input.setText(
                    f"{remains}")
            else:
                remains = remains - accrual - vacation_pay
                self.remains_input.setText(f"{remains}")
        except ValueError:
            self.remains_input.setText("-")

    def on_save(self):
        job = self.job_input.text().strip()

        if not job:
            QMessageBox.warning(self, "Ошибка", "Надо заполнить строчку 'Должность'!")
            return
        #try:
        vacation_pay = float(self.vacation_pay_input.text().replace(',', '.') or 0)
        accrual = float(self.accrual_input.text().replace(',', '.') or 0)
        remains = float(self.remains_input.text().replace(',', '.') or 0)
        #except ValueError:
            #QMessageBox.warning(self, "Ошибка", "Часы и стоимость должны быть числами!")
            #return

        if remains != 0:
            accrual = float(accrual) if accrual else 0.0
            vacation_pay = float(vacation_pay) if vacation_pay else 0.0
            remains = remains - accrual - vacation_pay

        date_str = self.date_input.date().toString("dd.MM.yyyy")
        employee_id = self.load_record()[0]
        fio = self.load_record()[1]
        hours = self.load_record()[2]
        price = self.load_record()[3]
        conn = sqlite3.connect("salary.db")
        cursor = conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO salary_data 
            (employee_id, fio, total_hours, 
            price_one_hour, job_title, 
            accrual, vacation_pay, remains, 
            record_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (employee_id, fio,
                  hours, price,
                  job, accrual,
                  vacation_pay, remains, date_str))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "успех", "Запись изменена!")
            self.accept()
        except Exception as e:
            conn.rollback()
            conn.close()
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить: {e}")
