from PySide6.QtWidgets import QLineEdit, QLabel, QPushButton
from ui.constants import (
    BIG_FONT_SIZE,
    SMALL_FONT_SIZE,
    MEDIUM_FONT_SIZE,
    TEXT_MARGIN,
    MINIMUM_WIDTH,
)
from PySide6.QtCore import Qt


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
        self.setProperty('cssClass', 'specialButton')
        self.setMinimumSize(75, 75)
