# dashboard.py
from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout
from crud_employee import CrudEmployee
from crud_doctors import CrudDoctors
from crud_has_sanctionreward import CrudHasSR
from analytics import AnalyticsWindow
from PySide6.QtCore import Qt

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("תפריט ראשי")
        self.setLayoutDirection(Qt.RightToLeft)

        layout = QVBoxLayout()
        buttons = [
            ("ניהול עובדים", CrudEmployee),
            ("ניהול רופאים", CrudDoctors),
            ("ניהול קנסות/בונוסים", CrudHasSR),
            ("דוחות וסטטיסטיקות", AnalyticsWindow)
        ]

        for label, cls in buttons:
            btn = QPushButton(label)
            btn.clicked.connect(lambda _, c=cls: self.open_window(c))
            layout.addWidget(btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_window(self, cls):
        self.child = cls(self)
        self.child.show()
