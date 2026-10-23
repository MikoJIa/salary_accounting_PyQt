from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QTabWidget, QWidget,
    QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt
from db_users import DataBase
from style_sheet.styles import ADMIN_WINDOW, ADMIN_BUTTON, ADMIN_APPROVE_BTN, REGECT_BTN, REFRESH_BTN, DELETE_BTN


class AdminWindow(QDialog):

    def __init__(self, db_account, parent=None):
        super().__init__(parent)
        self.db = db_account
        self.setWindowTitle("Панель администратора")
        self.setMinimumSize(900, 600)
        self.setup_ui()
        self.load_requests()
        self.load_users()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Панель администратора")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(ADMIN_WINDOW)
        layout.addWidget(title)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.requests_tab = QWidget()
        self.setup_requests_tab()
        self.tabs.addTab(self.requests_tab, "Заявки на регистрацию")

        self.users_tab = QWidget()
        self.setup_users_tab()
        self.tabs.addTab(self.users_tab, "Пользователи")

        self.close_btn = QPushButton("Закрыть")
        self.close_btn.clicked.connect(self.accept)
        self.close_btn.setStyleSheet(ADMIN_BUTTON)
        layout.addWidget(self.close_btn)

    def setup_requests_tab(self):
        layout = QVBoxLayout(self.requests_tab)

        self.requests_table = QTableWidget()
        self.requests_table.setColumnCount(3)
        self.requests_table.setHorizontalHeaderLabels(["ID", "Логин", "Дата создания"])
        self.requests_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.requests_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.requests_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self.requests_table)


        buttons = QHBoxLayout()

        self.approve_btn = QPushButton("Одобрить")
        self.approve_btn.clicked.connect(self.approve_selected)
        self.approve_btn.setStyleSheet(ADMIN_APPROVE_BTN)

        self.reject_btn = QPushButton("Отклонить")
        self.reject_btn.clicked.connect(self.reject_selected)
        self.reject_btn.setStyleSheet(REGECT_BTN)

        self.refresh_btn = QPushButton("Обновить")
        self.refresh_btn.clicked.connect(self.load_requests)
        self.refresh_btn.setStyleSheet(REFRESH_BTN)

        buttons.addWidget(self.approve_btn)
        buttons.addWidget(self.reject_btn)
        buttons.addStretch()
        buttons.addWidget(self.refresh_btn)
        layout.addLayout(buttons)

    def load_requests(self):
        requests = self.db.get_pending()
        self.requests_table.setRowCount(0)
        self.requests_table.setRowCount(len(requests))

        for row, req in enumerate(requests):
            for col, value in enumerate(req):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.requests_table.setItem(row, col, item)

    def approve_selected(self):
        row = self.requests_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите заявку!")
            return

        request_id = int(self.requests_table.item(row, 0).text())
        login = self.requests_table.item(row, 1).text()

        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Одобрить регистрацию пользователя '{login}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.db.approve_registration(request_id)
            if success:
                QMessageBox.information(self, "Успех", message)
                self.load_requests()
                self.load_users()
            else:
                QMessageBox.warning(self, "Ошибка", message)

    def reject_selected(self):
        row = self.requests_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите заявку!")
            return

        request_id = int(self.requests_table.item(row, 0).text())
        login = self.requests_table.item(row, 1).text()

        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Отклонить регистрацию пользователя '{login}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.db.reject_registration(request_id)
            if success:
                QMessageBox.information(self, "Успех", message)
                self.load_requests()
            else:
                QMessageBox.warning(self, "Ошибка", message)

    def setup_users_tab(self):
        layout = QVBoxLayout(self.users_tab)

        self.users_table = QTableWidget()
        self.users_table.setColumnCount(4)
        self.users_table.setHorizontalHeaderLabels(["ID", "Логин", "Админ", "Дата создания"])
        self.users_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.users_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.users_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self.users_table)

        buttons = QHBoxLayout()

        delete_btn = QPushButton("Удалить пользователя")
        delete_btn.clicked.connect(self.delete_selected_user)
        delete_btn.setStyleSheet(DELETE_BTN)

        refresh_btn = QPushButton("Обновить")
        refresh_btn.clicked.connect(self.load_users)
        refresh_btn.setStyleSheet(REFRESH_BTN)

        buttons.addWidget(delete_btn)
        buttons.addStretch()
        buttons.addWidget(refresh_btn)
        layout.addLayout(buttons)

    def load_users(self):
        users = self.db.get_all_users()
        self.users_table.setRowCount(0)
        self.users_table.setRowCount(len(users))

        for row, user in enumerate(users):
            user_id, login, is_admin, created = user
            values = [user_id, login, "Да" if is_admin else "Нет", created]
            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.users_table.setItem(row, col, item)

    def delete_selected_user(self):
        row = self.users_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя!")
            return

        user_id = int(self.users_table.item(row, 0).text())
        login = self.users_table.item(row, 1).text()

        if login == 'admin':
            QMessageBox.warning(self, "Ошибка", "Нельзя удалить главного администратора!")
            return

        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Удалить пользователя '{login}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.db.delete_user(user_id)
            if success:
                QMessageBox.information(self, "Успех", message)
                self.load_users()
            else:
                QMessageBox.warning(self, "Ошибка", message)