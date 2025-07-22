from ui.imports import (
    QLineEdit,
    QLabel,
    QPushButton,
    QGridLayout,
    Slot,
    Qt,
    QKeyEvent,
    Signal,
)  # noqa
from ui.constants import (
    BIG_FONT_SIZE,
    SMALL_FONT_SIZE,
    MEDIUM_FONT_SIZE,
    TEXT_MARGIN,
    MINIMUM_WIDTH,
)
from utils import is_num_or_dot, is_empty, is_valid_number
from ui.main_window import MainWindow
import math


# Caixa de texto de linha única
class Display(QLineEdit):
    eq_pressed = Signal()
    del_pressed = Signal()
    clear_pressed = Signal()

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

    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key

        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return]
        isDelete = key in [KEYS.Key_Backspace, KEYS.Key_Delete]
        isEsc = key in [KEYS.Key_Escape]

        if isEnter:
            self.eq_pressed.emit()
            return event.ignore()
        if isDelete:
            self.del_pressed.emit()
            return event.ignore()
        if isEsc:
            self.clear_pressed.emit()
            return event.ignore()
        # Lembre-se que caso não retorne o evento da superclasse,
        # nenhum imput é confirmado, apenas registrado conforme o
        # código antes disso.
        # return super().keyPressEvent(event)

        if is_empty(text):
            return event.ignore()
        print('Texto', text)


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
    def __init__(
        self, display: Display, info, window: 'MainWindow', *args, **kwargs
    ) -> None:
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
        self.window = window
        self.window = window
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

    def vou_apagar_voce(self):
        print('Signal recebido por "vou_apagar_voce" em', type(self).__name__)

    def _make_grid(self):
        self.display.eq_pressed.connect(self.vou_apagar_voce)
        self.display.del_pressed.connect(self.display.backspace)
        self.display.clear_pressed.connect(self.vou_apagar_voce)

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

        if text == '◄':
            self._connect_button_clicked(button, self.display.backspace)

        if text in '+-/*^':
            self._connect_button_clicked(
                button, self._set_display_slot(self._operator_clicked, button)
            )

        if text == '=':
            self._connect_button_clicked(button, self._eq)

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
            self._show_error(
                'Não foi inserido nenhum valor antes do operador.'
            )
            return

        if self._left is None:
            self._left = float(display_text)

        self._op = button_text
        self.equation = f'{self._left} {self._op} ??'

    def _eq(self):
        display_text = self.display.text()

        if not is_valid_number(display_text):
            self._show_error('nada válido para acrescentar')
            return

        self._right = float(display_text)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'error'
        try:
            if '^' in self.equation and isinstance(self._left, float):
                result = math.pow(self._left, self._right)
            else:
                result = eval(self.equation)
            self.info.setText(f'{self.equation} = {result}')
        except ZeroDivisionError:
            result = None
            self.info.setText(result)
            self._show_error('Não é possível dividir números por zero.')
        except OverflowError:
            result = None
            self.info.setText(result)
            self._show_error('A conta não pode ser realizada.')
        self.display.clear()
        self._left = result
        self._right = None

    def _make_dialog(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox

    def _show_error(self, text):
        msgBox = self._make_dialog(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        # Texto informatico dentro da msgBox
        # msgBox.setInformativeText('A descrição do erro será inserida aqui.')
        # Inserir botões alternativos na msgBox
        # msgBox.setStandardButtons(
        #     msgBox.StandardButton.Apply | msgBox.StandardButton.Cancel
        # )
        # Método padrão caso queira alterar o texto do button
        # msgBox.button(msgBox.StandardButton.Apply).setText('Aplicar')
        # msgBox.button(msgBox.StandardButton.Cancel).setText('Cancelar')
        msgBox.exec()
        # Verificando em qual botão o usuário clicou
        # if result == msgBox.StandardButton.Apply:
        #     print('Usuário clicou em aplicar')

        # elif result == msgBox.StandardButton.Cancel:
        #     print('Usuário clicou em cancelar')

    def _show_info(self, text):
        msgBox = self._make_dialog(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()
