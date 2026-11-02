from logica.tableroLogico import TableroLogico


class Juego:
    def __init__(self):
        self.tablero = 0

    def crear_tablero(self, fila, columna):
        self.tablero = TableroLogico(18, 14, 5, fila, columna)

    def evaluar_movimiento(self, fila, columna):
        if self.tablero == 0:
            self.crear_tablero(fila, columna)
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
