import sys

from PySide6 import QtWidgets
from qt_material import apply_stylesheet

from olx_contacts_scraping.main_window import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    apply_stylesheet(app, 'dark_blue.xml')
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
