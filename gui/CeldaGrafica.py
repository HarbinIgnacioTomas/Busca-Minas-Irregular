from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt


class CeldaGrafica(QPushButton):

    celda_click = pyqtSignal(int, int)

    VALORES = {
        -1 : "red;",
        0 : "black;",
        1 : "#2776F5;",
        2 : "#28B838;",
        3 : "#FF0000;",
        4 : "#11007A;",
        5 : "#7A0000;",
        6 : "#4E7E91;",
        7 : "#5B0080;",
        8 : "#000000;",
    }

    def __init__(self, tablero, pos_x, pos_y, fila, columna):
        super().__init__(tablero)
        self.fila = fila
        self.columna = columna
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.setGeometry(pos_x, pos_y, 50, 50)
        self.clicked.connect(self.mousePressEvent)
        self.setFont(QFont('Arial', 15))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.celda_click.emit(self.fila, self.columna)
        else:
            self.bandera()

    def cambiar_contenido(self, contenido):
        self.setEnabled(False)
        if contenido == 9:
            self.setStyleSheet("QPushButton:disabled {"
                               "background-color: none;}")
        elif contenido == 0 or contenido == -1:
            self.setText("X")
            self.setStyleSheet(f"color: {self.VALORES[contenido]}")
        else:
            self.setText(str(contenido))
            self.setStyleSheet(f"color: {self.VALORES[contenido]};"
                               "font-weight: bold;")

    def bandera(self):
        self.setText("B") if self.text() == "" else self.setText("")
