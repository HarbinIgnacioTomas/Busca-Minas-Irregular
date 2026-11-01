import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSignal

import random

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

class TableroGrafico(QWidget):
    def __init__(self, ventana, filas, columnas):
        super().__init__(ventana)
        self.filas = filas
        self.columnas = columnas
        self.setGeometry(0, 0, 700, 900)
        self.celdas = self.crear_celdas()

    def crear_celdas(self):
        celdas = [[] for _ in range(self.filas)]
        pos_y = 0
        for i in range (self.filas):
            pos_x = 0
            for j in range (self.columnas):
                celda = Celda (self, pos_x, pos_y, i, j)
                celdas[i].append(celda)
                pos_x += 50
            pos_y += 50
        return celdas

    def mostrar_celdas(self, posiciones, valores):
        pass
        for posicion, valor in zip(posiciones, valores):
            #print(self.celdas[posicion[0]][posicion[1]].pos_x, self.celdas[posicion[0]][posicion[1]].pos_y)
            self.celdas[posicion[0]][posicion[1]].cambiar_contenido(valor)


class Celda(QPushButton):

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

class Juego:
    def __init__(self):
        self.tablero = 0

    def evaluar_movimiento(self, fila, columna):
        if self.tablero == 0:
            self.tablero = TableroLogico(18, 14, 40, fila, columna)
        celdas = []
        valores = []
        estado = 0
        if self.tablero.es_mina(fila, columna):
            estado = -1
            celdas.append((fila, columna))
            valores.append(-1)
            return celdas, valores, estado
        else:
            celdas_a_mostrar = self.tablero.celdas_a_mostrar(fila, columna)
            for celda in celdas_a_mostrar[0]:
                celdas.append(celda)
            for valor in celdas_a_mostrar[1]:
                valores.append(valor)
            estado = 1 if self.tablero.celdas_resantes == 0 else 0

            print()

            z = 0

            for line in self.tablero.celdas:
                print(line)
            # for line in celdas_a_mostrar[0]:
            #     print(f"f:{line[0]} c: {line[1]} v:{celdas_a_mostrar[1][z]}")
            #     z += 1
            #print(celdas_a_mostrar)
            return celdas, valores, estado


class TableroLogico:
    def __init__(self, filas, columnas, cant_minas, primera_fila, primera_columna):
        self._celdas_restantes = filas * columnas - cant_minas
        self.filas = filas
        self.columnas = columnas
        self.cant_minas = cant_minas
        self.primera_fila = primera_fila
        self.primera_columna = primera_columna
        self.minas = []
        self.celdas = self.crear_tablero()
        #print(self.minas)
        for line in self.celdas:
            print(line)

    @property
    def celdas_resantes(self):
        return self._celdas_restantes

    def crear_tablero(self):
        celdas = [[] for _ in range(self.filas)]
        for i in range(self.filas):
            for j in range(self.columnas):
                celdas[i].append(9)
        self.colocar_minas_y_numeros(celdas)
        return celdas

    def colocar_minas_y_numeros(self, celdas):
        i = 0

        evitar_minas = []
        fila_desde = self.primera_fila - 1
        fila_hasta = self.primera_fila + 2
        columna_desde = self.primera_columna - 1
        columna_hasta = self.primera_columna + 2


        for fila in range(fila_desde, fila_hasta):
            for columna in range(columna_desde, columna_hasta):
                print(fila, columna)
                evitar_minas.append((fila, columna))

        print(evitar_minas)

        while i < self.cant_minas:
            fila = random.randrange(len(celdas))
            columna = random.randrange(len(celdas[0]))
            if celdas[fila][columna] != 0 and (fila, columna) not in evitar_minas:
                celdas[fila][columna] = 0
                self.minas.append((fila, columna))
                self.calcular_numeros(celdas, fila, columna)
                i += 1

    def calcular_numeros(self, celdas, fila, columna):
        columna_aux = columna - 1
        fila -= 1
        for i in range (3):
            columna = columna_aux
            for j in range(3):
                if fila < 0 or fila > self.filas - 1 or columna < 0 or columna > self.columnas - 1:
                    columna += 1
                elif celdas[fila][columna] == 0:
                    columna += 1
                else:
                    if celdas[fila][columna] == 9:
                        celdas[fila][columna] = 0
                    celdas[fila][columna] += 1
                    columna += 1
            fila += 1

    def es_mina(self, fila, columna):
        return True if self.celdas[fila][columna] == 0 else False

    def celdas_a_mostrar(self, fila, columna):
        celdas = []
        valores = []
        if self.celdas[fila][columna] != 9:
            self._celdas_restantes -= 1
            celdas.append((fila, columna))
            valores.append(self.celdas[fila][columna])
            self.celdas[fila][columna] = self.celdas[fila][columna] * -1
        else:
            self.cascada(fila, columna, celdas, valores)
        return celdas, valores


    def cascada(self, fila, columna, celdas, valores):
        fila -= 1
        columna_aux = columna - 1

        for i in range(3):
            columna = columna_aux
            for j in range(3):
                if fila < 0 or fila > self.filas - 1 or columna < 0 or columna > self.columnas - 1:
                    columna += 1
                elif self.celdas[fila][columna] <= 0:
                     columna += 1
                else:
                    self._celdas_restantes -= 1
                    celdas.append((fila, columna))
                    valores.append(self.celdas[fila][columna])

                    if self.celdas[fila][columna] == 9:
                        self.celdas[fila][columna] = self.celdas[fila][columna] * -1
                        self.cascada(fila, columna, celdas, valores)
                    else:
                        self.celdas[fila][columna] = self.celdas[fila][columna] * -1
                    columna += 1
            fila += 1

        return celdas, valores

def main():
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec_())
    pass

if __name__ == '__main__':
    main()
#
# class BotonPrueba(QPushButton):
#
#     click = pyqtSignal(str)
#
#     def __init__(self, parent=None):
#         super().__init__("boton", parent)
#         self.setFont(QFont('Arial', 10))
#         self.setGeometry(100, 100, 200, 100)
#
#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.click.emit("izquierdo")
#         elif event.button() == Qt.RightButton:
#             self.click.emit("derecho")