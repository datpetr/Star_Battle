import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('menu.ui', self)
        # подгружаем файл из designer

        # подключаем кнопки
        self.play.clicked.connect(self.Show_lvl)
        self.rules.clicked.connect(self.Show_rules)

    def Show_lvl(self):
        self.lvl = LEVEL()
        self.lvl.show()

    def Show_rules(self):
        self.rules = Rules()
        self.rules.show()


class Rules(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu = Menu()
        uic.loadUi('rules.ui', self)


class LEVEL(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('levels.ui', self)
        # подгружаем файл из designer

        # подключаем кнопки
        self.lvl1.clicked.connect(self.Show_lvl1)
        self.lvl2.clicked.connect(self.Show_lvl2)
        self.lvl3.clicked.connect(self.Show_lvl3)

    def Show_lvl1(self):
        import main_game

    def Show_lvl2(self):
        import main_game

    def Show_lvl3(self):
        import main_game


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.exit(app.exec_())
