import random
from logica.celdaLogica import celdaLogica


class tableroLogicoIrregular:
    def __init__(self, filas, columnas, cant_minas, primera_fila, primera_columna, cant_celdas_irregulares):
        self.filas = filas
        self.columnas = columnas
        self.primera_fila = primera_fila
        self.primera_columna = primera_columna
        self.cant_minas = cant_minas
        self.minas = []
        self.tablero = self.crear_tablero()
        self.celdas = self.definir_celdas(filas, columnas, cant_celdas_irregulares)

    def crear_tablero(self):
        tablero = [[] for _ in range(self.filas)]
        for i in range(self.filas):
            for j in range(self.columnas):
                tablero[i].append(9)
        #self.colocar_minas_y_numeros(tablero)
        return tablero

    #guarda cada coordenada (key: (fila, columna) en un diccionario asociada a su celda (objeto)
    # (4 coordenadas para las grandes, 1 para las clasicas)
    def definir_celdas(self, filas, columnas, cant_irregulares=10):
        celdas = {}
        celdas_aux = set()
        for i in range(cant_irregulares):
            coordenadas = []
            fila_rand = random.randint(0, filas - 2)
            columna_rand = random.randint(0, columnas - 2)

            #valida que la celda origen del bloque 2*2 no caiga ni genere un bloque que colisione con otros
            #y la desplaza lo necesario (para una grilla de 18*14 no se debe pasar de 23 bloques por el umbral minimo)
            while (fila_rand, columna_rand) in celdas_aux:
                if columna_rand < columnas - 2:
                    columna_rand += 1
                else:
                    columna_rand = 0
                    if fila_rand < filas - 2:
                        fila_rand += 1
                    else:
                        fila_rand = 0

            columna_aux = columna_rand
            fila_aux = fila_rand
            #guarda las 9 coordenadas necesarias para validar que no se pisen los bloques 2*2
            #y las 4 coordenadas de las celdas 2*2 en el diccionario
            for c in range(columna_rand-1, columna_rand+2):
                for f in range(fila_rand-1, fila_rand+2):
                    celdas_aux.add((f, c))
                    if 0 <= f < filas and 0 <= c < columnas:
                        celdas_aux.add((f, c))
                        if c >= columna_aux and f >= fila_aux:
                            coordenadas.append((f, c))

            #asocia las 4 coordenadas creando un objeto celda
            #y guarda las coordenadas como clave que apuntan a su misma celda
            nueva_celda = celdaLogica(coordenadas)
            for coordenada in coordenadas:
                celdas[coordenada] = nueva_celda

        for fila in range(filas):
            for columna in range(columnas):
                if (fila, columna) not in celdas:
                    nueva_celda = celdaLogica([fila, columna])
                    celdas[(fila, columna)] = nueva_celda

        self.definir_vecinos(celdas)

        #print(celdas)
        return celdas

    def definir_vecinos(self, celdas):
        for coordenada, celda in celdas.items():
            fila, columna = coordenada
            for f in range(fila - 1, fila + 2):
                for c in range(columna - 1, columna + 2):
                    if 0 <= f < self.filas and 0 <= c < self.columnas:
                        celda_vecina = celdas[(f, c)]
                        if celda_vecina is not celda:
                            celda.vecinas.add(celda_vecina)

    def colocar_minas_y_numeros(self, celdas):
        i = 0

        fila_desde = self.primera_fila - 1
        fila_hasta = self.primera_fila + 2
        columna_desde = self.primera_columna - 1
        columna_hasta = self.primera_columna + 2

        for fila in range(fila_desde, fila_hasta):
            for columna in range(columna_desde, columna_hasta):
                if 0 <= fila < self.filas and 0 <= columna < self.columnas:
                    celdas[(fila, columna)].celda_segura = True

        while i < self.cant_minas:
            fila = random.randrange(self.filas)
            columna = random.randrange(self.columnas)

            if not celdas[(fila, columna)].es_mina and not celdas[(fila, columna)].celda_segura:
                celdas[(fila, columna)].es_mina = True
                self.minas.append(celdas[(fila, columna)])
                self.calcular_numeros(celdas[(fila, columna)])
                i += 1

    def calcular_numeros(self, celda_mina):
        for vecina in celda_mina.vecinas:
            if not vecina.es_mina:
                if vecina.valor is None:
                    vecina.valor = 0
                vecina.valor += 1


    #metodo para comprobar la creacion correcta del tablero y disposicion de minas/valores
    def imprimir_tablero(self, celdas):
        for f in range(self.filas):
            fila_str = ""
            for c in range(self.columnas):
                celda = celdas[(f, c)]
                if celda.es_mina:
                    fila_str += " M "
                elif celda.valor is None:
                    fila_str += " V "
                else:
                    fila_str += f" {celda.valor} "
            print(fila_str)
