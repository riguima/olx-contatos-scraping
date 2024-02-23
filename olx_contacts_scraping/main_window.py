from PySide6 import QtCore, QtWidgets

from olx_contacts_scraping.browser import Browser
from olx_contacts_scraping.consts import STATES


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        self.setFixedSize(600, 600)
        with open('styles.qss', 'r') as file:
            self.setStyleSheet(file.read())

        self.browser = Browser('default_user_data', headless=False)

        self.state_label = QtWidgets.QLabel('Estado:')
        self.state_combobox = QtWidgets.QComboBox()
        self.state_combobox.addItems(STATES)
        self.state_layout = QtWidgets.QHBoxLayout()
        self.state_layout.addWidget(self.state_label)
        self.state_layout.addWidget(self.state_combobox)

        self.generate_spreadsheet_button = QtWidgets.QPushButton(
            'Gerar Planilha'
        )
        self.generate_spreadsheet_button.clicked.connect(
            self.generate_spreadsheet
        )

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.state_layout)

    @QtCore.Slot()
    def generate_spreadsheet(self):
        pass
