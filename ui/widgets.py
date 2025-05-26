from ui.imports import (
    QLineEdit,
    QLabel,
    QPushButton,
    QGridLayout,
    Slot,
    Qt,
)  # noqa
from ui.constants import (
    BIG_FONT_SIZE,
    SMALL_FONT_SIZE,
    MEDIUM_FONT_SIZE,
    TEXT_MARGIN,
    MINIMUM_WIDTH,
)
from utils import is_num_or_dot, is_empty


# Caixa de texto de linha única
class Display(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_style()

    def config_style(self):
        # gera uma lista com a margem para os 4 lados
        margins = [TEXT_MARGIN for _ in range(4)]
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px')
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setMinimumWidth(MINIMUM_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*margins)


# Label com informações não editáveis pelo usuário
class Info(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_style()

    def config_style(self):
        self.setStyleSheet(f'font-size: {SMALL_FONT_SIZE}px')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)


# Método alternativo para se iniciar a classe
# class Info(QLabel):
#     def __init__(self, text: str, parent: QWidget | None = None) -> None:
#         super().__init__(text, parent)


# Botão interativo
class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_style()

    def config_style(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)


class ButtonsGrid(QGridLayout):
    def __init__(self, display: Display, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._grid_mask = [
            ['C', '◄', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['', '0', '.', '='],
        ]
        self.display = display
        self._makegrid()

    def _makegrid(self):
        for row_number, row in enumerate(self._grid_mask):
            for column_number, button_text in enumerate(row):
                button = Button(button_text)
                self.addWidget(button, row_number, column_number)

                if not is_num_or_dot(button_text) and not is_empty(
                    button_text
                ):
                    button.setProperty('cssClass', 'specialButton')
                button_slot = self._set_button_display_slot(
                    self._insert_button_text_to_display,
                    button,
                )
                button.clicked.connect(button_slot)

    def _set_button_display_slot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)

        return realSlot

    def _insert_button_text_to_display(self, button):
        self.display.setText(button.text())
