import sys
from PyQt5.QtWidgets import QApplication
from app_window import MainApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
