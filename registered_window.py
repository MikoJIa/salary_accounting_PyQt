from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QDialog, QLineEdit, QHBoxLayout, QPushButton
from style_sheet.styles import REGISTRATION_WINDOW_STYLE
from datetime import datetime


class RegisteredWindow(QDialog):

    def __init__(self, db_account, parent=None):
        super().__init__(parent)
        self.db_account = db_account
        self.new_login = ''
        self.ui_setup()

    def ui_setup(self):
        self.setWindowTitle('Окно регистрации пользователя')
        self.setFixedSize(550, 450)
        self.setStyleSheet(REGISTRATION_WINDOW_STYLE)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 35, 50, 35   )
        main_layout.setSpacing(20)

        title_label = QLabel('Регистрация')
        title_label.setObjectName('title_label')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        subtitle_label = QLabel('Создайте нового пользователя')
        subtitle_label.setObjectName('subtitle_label')
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle_label)

        login_layout = QHBoxLayout()
        login_label = QLabel('Новый логин')
        login_label.setStyleSheet("font-size: 16px; font-weight: 200;")
        self.login_input = QLineEdit(self)
        self.login_input.setObjectName('login_input')
        self.login_input.setPlaceholderText("Введите новый логин")
        self.login_input.installEventFilter(self)
        login_layout.addWidget(login_label)
        login_layout.addWidget(self.login_input)
        main_layout.addLayout(login_layout)

        password_layout = QHBoxLayout()
        password_label = QLabel('Новый пароль')
        password_label.setStyleSheet("font-size: 16px; font-weight: 200;")
        self.password_input = QLineEdit(self)
        self.password_input.setObjectName('password_input')
        self.password_input.setPlaceholderText("Введите новый пароль")
        self.password_input.installEventFilter(self)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        main_layout.addLayout(password_layout)

        password_confirmation_layout = QHBoxLayout()
        password_confirmation_label = QLabel("Подтверждение пароля")
        password_confirmation_label.setStyleSheet("font-size: 16px; font-weight: 200;")
        self.password_confirmation_input = QLineEdit(self)
        self.password_confirmation_input.setObjectName('password_confirmation_input')
        self.password_confirmation_input.setPlaceholderText("Введите повторно пароль")
        self.password_confirmation_input.installEventFilter(self)
        password_confirmation_layout.addWidget(password_confirmation_label)
        password_confirmation_layout.addWidget(self.password_confirmation_input)
        main_layout.addLayout(password_confirmation_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        self.btn_create = QPushButton("Создать")
        self.btn_create.setObjectName('btn_create')
        self.btn_create.clicked.connect(self.get_new_login)

        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.setObjectName('btn_cancel')
        self.btn_cancel.clicked.connect(self.reject)

        buttons_layout.addWidget(self.btn_create)
        buttons_layout.addWidget(self.btn_cancel)
        main_layout.addLayout(buttons_layout)

        self.success_label = QLabel("Регистрация прошла успешна!")
        self.success_label.setObjectName('success_label')
        self.success_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.success_label.hide()

        self.error_label = QLabel("Произошла ошибка регистрации!!!")
        self.error_label.setObjectName('error_label')
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.hide()

        main_layout.addWidget(self.success_label)
        main_layout.addWidget(self.error_label)

        self.setLayout(main_layout)

    def view_success(self, message):
        self.success_label.setText(message)
        self.success_label.show()
        self.success_label.hide()
        QTimer.singleShot(2000, self.cancellation)

    def view_error(self, message):
        self.error_label.setText(message)
        self.error_label.show()
        self.error_label.hide()
        QTimer.singleShot(2000, self.error_label.hide)

    def get_new_login(self):
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()
        confirmation_pass = self.password_confirmation_input.text().strip()

        if len(login) == 0 or len(login) < 5:
            self.view_error("Логин должен содержать не менее 5 символов!!!")
            return
        if len(password) == 0 or len(password) < 5:
            self.view_error("Логин должен содержать минимум 5 символов!!!")
            return
        if password != confirmation_pass:
            self.view_error("Пароли не совпадают!!!")
            return
        if self.db_account.check_user(login):
            self.view_error(f"Пользователь с логином {login} уже существует!!!")

        success, message = self.db_account.add_user(login, password)
        if success:
            self.view_success(message)
            self.new_login = login
        else:
            self.view_error(message)

    # def create_new_user(self):
    #     pass

    def cancellation(self):
        pass