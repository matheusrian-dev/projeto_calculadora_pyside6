import sys

from ui.widgets import Display, Info, ButtonsGrid
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

    info = Info('Sua conta')
    window.add_widget_to_vlayout(info)

    # É possível settar um texto inicial ao inserir
    # string no Display()
    display = Display()
    display.setPlaceholderText('Digite alguma coisa')
    window.add_widget_to_vlayout(display)

    buttons_grid = ButtonsGrid(display, info)
    window.v_layout.addLayout(buttons_grid)

    icon = QIcon(WINDOW_ICON_PATH_STR)
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    window.adjust_fixed_size()
    window.show()

    app.exec()
