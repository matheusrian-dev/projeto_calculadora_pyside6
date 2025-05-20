import sys

from PySide6.QtWidgets import QApplication, QLabel
from display import Display
from PySide6.QtGui import QIcon
from main_window import MainWindow
from paths import WINDOW_ICON_PATH_STR


def temp_label(texto):
    lbl = QLabel(texto)
    lbl.setStyleSheet('font-size: 40px')
    return lbl


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    # É possível settar um texto inicial ao inserir
    # string no Display()
    display = Display()
    display.setPlaceholderText('Digite alguma coisa')
    window.addToVLayout(display)

    icon = QIcon(WINDOW_ICON_PATH_STR)
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    window.addToVLayout(temp_label('Texto 1'))

    window.adjustFixedSize()
    window.show()

    app.exec()
