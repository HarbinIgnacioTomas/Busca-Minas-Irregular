import random


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
