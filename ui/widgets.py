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
from utils import is_num_or_dot, is_empty, is_valid_number


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
    def __init__(self, display: Display, info, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._grid_mask = [
            ['C', '◄', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['', '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self._equation = ''
        self._equation_initial_value = 'Sua conta'
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equation_initial_value
        self._make_grid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _make_grid(self):
        for row_number, row in enumerate(self._grid_mask):
            for column_number, button_text in enumerate(row):
                button = Button(button_text)
                self.addWidget(button, row_number, column_number)

                if not is_num_or_dot(button_text) and not is_empty(
                    button_text
                ):
                    button.setProperty('cssClass', 'specialButton')
                    self._config_special_button(button)
                slot = self._set_display_slot(
                    self._insert_button_text_to_display,
                    button,
                )
                self._connect_button_clicked(button, slot)

    def _connect_button_clicked(self, button, slot):
        button.clicked.connect(slot)

    def _config_special_button(self, button):
        text = button.text()
        if text == 'C':
            self._connect_button_clicked(button, self._clear)

        if text in '+-/*':
            self._connect_button_clicked(
                button, self._set_display_slot(self._operator_clicked, button)
            )

    def _set_display_slot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)

        return realSlot

    def _insert_button_text_to_display(self, button):
        button_text = button.text()
        new_display_value = self.display.text() + button_text

        if not is_valid_number(new_display_value):
            return

        self.display.setText(new_display_value)

    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        # reseta a label que exibe a equação
        self.equation = self._equation_initial_value
        self.display.clear()

    def _operator_clicked(self, button):
        button_text = button.text()  # +-/*
        display_text = self.display.text()  # número _left
        self.display.clear()

        if not is_valid_number(display_text) and self._left is None:
            print('Não foi inserido nenhum valor antes do operador.')
            return

        if self._left is None:
            self._left = float(display_text)

        self._op = button_text
        self.equation = f'{self._left} {self._op} ??'
