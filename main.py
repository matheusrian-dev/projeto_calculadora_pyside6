import sys

from PySide6.QtWidgets import QApplication, QLabel
from ui.widgets import Display, Info
from PySide6.QtGui import QIcon
from ui.main_window import MainWindow
from resources.paths import WINDOW_ICON_PATH_STR
from ui.styles import setupTheme


def temp_label(texto):
    lbl = QLabel(texto)
    lbl.setStyleSheet('font-size: 40px')
    return lbl


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    setupTheme(app)

    info = Info('2.0 ^ 10.0 = 1024')
    window.addToVLayout(info)

    # É possível settar um texto inicial ao inserir
    # string no Display()
    display = Display()
    display.setPlaceholderText('Digite alguma coisa')
    window.addToVLayout(display)

    icon = QIcon(WINDOW_ICON_PATH_STR)
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    window.adjustFixedSize()
    window.show()

    app.exec()
