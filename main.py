import sys
from PySide6 import QtWidgets

from utils.styles import setup_styles
from views.main_window import MainWindow


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    setup_styles(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())