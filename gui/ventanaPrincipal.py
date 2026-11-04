from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import Qt

from gui.tableroGrafico import TableroGrafico
from logica.juegoViejo import Juego


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(550, 100, 700, 900)
        self.tablero = TableroGrafico(self, 18, 14)
        self.juego = Juego()
        self.presionar_celda()
        self.texto_final = QLabel(self)
        self.texto_final.setGeometry((self.rect().width() - 500) // 2, (self.rect().height() - 200) // 2, 500, 200)
        self.texto_final.setStyleSheet("background-color: white;"
                                       "border-radius: 25px;"
                                       "border-style: solid;"
                                       "border-width: 15px;"
                                       "font-weight: bold;"
                                       "border-color: black;")
        self.texto_final.setFont(QFont('Arial', 50))
        self.texto_final.setAlignment(Qt.AlignCenter)
        self.texto_final.hide()

    def presionar_celda(self):
        for fila in self.tablero.celdas:
            for celda in fila:
                celda.celda_click.connect(self.celda_presionada)

    def celda_presionada(self, fila, columna):
        movimiento = self.juego.evaluar_movimiento(fila, columna)
        print(self.juego.tablero.celdas_resantes)
        self.tablero.mostrar_celdas(movimiento[0], movimiento[1])
        if movimiento[2] != 0:
            if (fila, columna) in self.juego.tablero.minas:
                self.juego.tablero.minas.remove((fila, columna))
            self.mostrar_resultado(movimiento[2])

    def mostrar_resultado(self, resultado):
        if resultado == -1:
            self.tablero.mostrar_celdas(self.juego.tablero.minas, [0 for _ in range(len(self.juego.tablero.minas))])
        self.texto_final.setText("Ganaste" if resultado == 1 else "Perdiste")
        self.texto_final.show()
        self.tablero.bloquear_celdas()
