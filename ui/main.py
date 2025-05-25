import sys

from ui.widgets import Display, Info, Button
from ui.main_window import MainWindow
from resources.paths import WINDOW_ICON_PATH_STR
from ui.styles import setup_theme
from ui.imports import QApplication, QLabel, QIcon  # noqa


def temp_label(texto):
    lbl = QLabel(texto)
    lbl.setStyleSheet('font-size: 40px')
    return lbl


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    setup_theme(app)

    info = Info('2.0 ^ 10.0 = 1024')
    window.add_to_vlayout(info)

    # É possível settar um texto inicial ao inserir
    # string no Display()
    display = Display()
    display.setPlaceholderText('Digite alguma coisa')
    window.add_to_vlayout(display)

    button = Button('Texto do botão')
    window.add_to_vlayout(button)

    icon = QIcon(WINDOW_ICON_PATH_STR)
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    window.adjust_fixed_size()
    window.show()

    app.exec()
