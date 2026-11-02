from PyQt5.QtWidgets import QWidget

from gui.CeldaGrafica import CeldaGrafica


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
                celda = CeldaGrafica (self, pos_x, pos_y, i, j)
                celdas[i].append(celda)
                pos_x += 50
            pos_y += 50
        return celdas

    def mostrar_celdas(self, posiciones, valores):
        pass
        for posicion, valor in zip(posiciones, valores):
            #print(self.celdas[posicion[0]][posicion[1]].pos_x, self.celdas[posicion[0]][posicion[1]].pos_y)
            self.celdas[posicion[0]][posicion[1]].cambiar_contenido(valor)

    def bloquear_celdas(self):
        for fila in self.celdas:
            for celda in fila:
                celda.setEnabled(False)
