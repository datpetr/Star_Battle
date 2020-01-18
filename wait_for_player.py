import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('menu.ui', self)
        # подгружаем файл из designer

        # подключаем кнопки
        self.continue_2.clicked.connect(self.Continue)
        self.return_2.clicked.connect(self.Back)

    def Continue(self):
        pass

    def Back(self):
        import menu


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.exit(app.exec_())