from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.central_widget = QWidget()
        self.v_layout = QVBoxLayout()

        self.central_widget.setLayout(self.v_layout)
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle('Calculadora')

    def adjust_fixed_size(self):
        # Última coisa a ser feita
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    # Não é uma boa prática manter acessos aninhados,
    # caso veja que há mais de um (objeto1.objeto2.funcao1),
    # crie um método para implementar esse acesso.
    def add_to_vlayout(self, widget: QWidget):
        self.v_layout.addWidget(widget)
