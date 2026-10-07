from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLineEdit, QLabel, QDialog, QVBoxLayout, QProgressBar
from style_sheet.styles import STYLE_QDIALOG_WINDOW, INPUT_STYLE
from db_users import DataBase
from registered_window import RegisteredWindow


class LoginWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.db_account = DataBase()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Вход в программу")
        self.setFixedSize(550, 450)
        #self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet(STYLE_QDIALOG_WINDOW)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 40, 50, 40)
        main_layout.setSpacing(20)

        title_label = QLabel('Вход в программу учёта данных')
        title_label.setObjectName('title_label')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        subtitle_label = QLabel("Введите логин и пароль")
        subtitle_label.setObjectName('subtitle_label')
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle_label)

        login_layout = QHBoxLayout()
        login_label = QLabel("Логин")
        login_label.setStyleSheet("font-size:14px; font-weight:400;")
        self.login_input = QLineEdit()
        self.login_input.installEventFilter(self)
        login_layout.addWidget(login_label)
        login_layout.addWidget(self.login_input)
        main_layout.addLayout(login_layout)

        password_layout = QHBoxLayout()
        password_label = QLabel("Пароль")
        password_label.setStyleSheet("font-size:14px; font-weight:400;")
        self.password_input = QLineEdit()
        #self.password_input.setEchoMode(QLineEdit.Password) #  для того что бы пароль вводился звёздочками
        self.password_input.installEventFilter(self) # перехватывает и обробатывает события: клик мыши, нажатия клавишь и т.д.
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        main_layout.addLayout(password_layout)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.hide()
        main_layout.addWidget(self.progress_bar)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)

        self.reg_button = QPushButton("Регистрация")
        self.reg_button.setObjectName('reg_button')
        self.reg_button.clicked.connect(self.open_registration)

        self.log_button = QPushButton("Войти")
        self.log_button.setObjectName('log_button')
        self.log_button.clicked.connect(self.try_login)

        btn_layout.addWidget(self.reg_button)
        btn_layout.addWidget(self.log_button)
        main_layout.addLayout(btn_layout)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #78909C; font-size: 11px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)

        self.error_label = QLabel("")
        self.error_label.setObjectName("error")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.hide()
        main_layout.addWidget(self.error_label)

        self.setLayout(main_layout)


    def open_registration(self):
        reg_account = RegisteredWindow(self.db_account, self)
        if reg_account.exec() == QDialog.DialogCode.Accepted: # делаем проверку о успешной регистрации
            new_login = reg_account.get_new_login()
            if new_login:
                self.login_input.setText(new_login)
                self.password_input.clear()
                self.error_label.hide()



    def try_login(self):
        LOGIN = self.login_input.text().strip()
        PASSWORD = self.password_input.text().strip()

        if LOGIN == "" or PASSWORD == "":
            self.show_e("Необходимо заполнить все поля!!!")
            return

        self.progress_bar.show()
        self.progress_bar.setRange(0, 10)
        self.log_button.setEnabled(False)
        self.reg_button.setEnabled(False)

    def show_e(self, text):
        self.error_label.setText(text)
        self.error_label.show()
        QTimer.singleShot(2000, self.error_label.hide)

    def end_login(self, login, password):
        self.progress_bar.hide()
        self.log_button.setEnabled(True)
        self.reg_button.setEnabled(True)

        if not self.db_account.check_user(login):
            self.show_e(f"Пользователь {login} не найден!!!")
            return
        if self.db_account.verification(login, password):
            self.status_label.setText('Вход успешен!')
            self.status_label.setStyleSheet('color: #78909C; font-size: 11px;')
            self.accept()
        else:
            self.show_e("Пароль неверен!")
            self.password_input.clear()
            self.password_input.setFocus()

    def get_credentials(self):
        return self.login_input.text(), self.password_input.text()