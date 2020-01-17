import sys
import csv
import xlsxwriter
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication, QMainWindow
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QFileDialog


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('menu.ui', self)
        # подгружаем файл из designer

        # подключаем кнопки
        self.play.clicked.connect(self.chose_lvl)
        self.rules.clicked.connect(self.show_rules)

        def show_rules(self):
            uic.loadUi('rules.ui', self)

        def play(self):
            self.LEVEL(self, '').show()


class LEVEL(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('levels.ui', self)
        # подгружаем файл из designer

        # подключаем кнопки
        self.lvl1.clicked.connect(self.chose_lvl1)
        self.lvl2.clicked.connect(self.chose_lvl1)
        self.lvl3.clicked.connect(self.chose_lvl1)

    def chose_lvl1(self):
        pass

    def chose_lvl2(self):
        pass

    def chose_lvl3(self):
        pass