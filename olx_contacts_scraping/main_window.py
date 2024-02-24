import pandas as pd
from itertools import count
from PySide6 import QtCore, QtWidgets, QtGui
from pathlib import Path

from olx_contacts_scraping.browser import Browser
from olx_contacts_scraping.consts import CATEGORIES, STATES


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 200)
        with open('styles.qss', 'r') as file:
            self.setStyleSheet(file.read())

        self.message_box = QtWidgets.QMessageBox()

        self.browser = Browser(headless=False)

        self.ad_type_label = QtWidgets.QLabel('Tipo de anúncio:')
        self.ad_type_combobox = QtWidgets.QComboBox()
        self.ad_type_combobox.addItems(['Profissional', 'Particular'])
        self.ad_type_layout = QtWidgets.QHBoxLayout()
        self.ad_type_layout.addWidget(self.ad_type_label)
        self.ad_type_layout.addWidget(self.ad_type_combobox)

        self.state_label = QtWidgets.QLabel('Estado:')
        self.state_combobox = QtWidgets.QComboBox()
        self.state_combobox.addItems(list(STATES.values()))
        self.state_layout = QtWidgets.QHBoxLayout()
        self.state_layout.addWidget(self.state_label)
        self.state_layout.addWidget(self.state_combobox)

        self.category_label = QtWidgets.QLabel('Categoria:')
        self.category_combobox = QtWidgets.QComboBox()
        self.category_combobox.addItems(list(CATEGORIES.values()))
        self.category_layout = QtWidgets.QHBoxLayout()
        self.category_layout.addWidget(self.category_label)
        self.category_layout.addWidget(self.category_combobox)

        self.page_label = QtWidgets.QLabel('Página inicio:')
        self.page_input = QtWidgets.QLineEdit()
        self.page_input.setText('1')
        self.page_input.setValidator(QtGui.QIntValidator())
        self.page_layout = QtWidgets.QHBoxLayout()
        self.page_layout.addWidget(self.page_label)
        self.page_layout.addWidget(self.page_input)

        self.generate_csv_button = QtWidgets.QPushButton('Gerar CSV')
        self.generate_csv_button.clicked.connect(self.generate_csv)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addLayout(self.ad_type_layout)
        self.main_layout.addLayout(self.state_layout)
        self.main_layout.addLayout(self.category_layout)
        self.main_layout.addLayout(self.page_layout)
        self.main_layout.addWidget(self.generate_csv_button)

    @QtCore.Slot()
    def generate_csv(self):
        state = list(STATES.keys())[self.state_combobox.currentIndex()]
        category = list(CATEGORIES.keys())[
            self.category_combobox.currentIndex()
        ]
        csv_path = f'result-{category}-{state}.csv'
        for page in count(int(self.page_input.text())):
            contacts_infos = self.browser.get_contacts_infos(
                self.ad_type_combobox.currentText(), state, category, page
            )
            if not contacts_infos:
                break
            dataframe = pd.DataFrame.from_dict(contacts_infos)
            if Path(csv_path).exists():
                dataframe_csv = pd.read_csv(csv_path)
                final_dataframe = pd.concat([dataframe_csv, dataframe])
                final_dataframe.to_csv(csv_path, index=False)
            else:
                dataframe.to_csv(csv_path, index=False)
        self.message_box.setText('Finalizado!')
        self.message_box.show()
