from PySide6.QtWidgets import QApplication
from login import LoginWindow
from dashboard import Dashboard
import sys

def main():
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QWidget {
            font-family: "Segoe UI", sans-serif;
            font-size: 14px;
            direction: rtl;
        }

        QPushButton {
            padding: 8px 16px;
            border-radius: 8px;
            background-color: #2980b9;
            color: white;
        }

        QPushButton:hover {
            background-color: #3498db;
        }

        QLineEdit {
            padding: 6px;
            border: 1px solid #ccc;
            border-radius: 6px;
        }

        QLabel {
            font-weight: bold;
        }

        QTableWidget {
            border: 1px solid #ddd;
            alternate-background-color: #f9f9f9;
        }

        QHeaderView::section {
            background-color: #2980b9;
            color: white;
            padding: 4px;
        }
    """)

    dash = Dashboard()
    login = LoginWindow(on_success=dash.show)
    login.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
