from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt
from db import get_conn

class LoginWindow(QWidget):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.setWindowTitle("התחברות")
        self.setLayoutDirection(Qt.RightToLeft)

        self.user = QLineEdit(placeholderText="שם משתמש")
        self.pwd = QLineEdit(placeholderText="סיסמה", echoMode=QLineEdit.Password)
        btn = QPushButton("התחבר")
        btn.clicked.connect(self.try_login)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("ברוך הבא"))
        layout.addWidget(self.user)
        layout.addWidget(self.pwd)
        layout.addWidget(btn)

    def try_login(self):
        with get_conn() as cur:
            cur.execute("SELECT 1 FROM staff_users WHERE username=%s AND pwd_hash=crypt(%s, pwd_hash)",
                        (self.user.text(), self.pwd.text()))
            if cur.fetchone():
                self.on_success()
                self.close()
            else:
                QMessageBox.warning(self, "שגיאה", "שם משתמש או סיסמה שגויים")
