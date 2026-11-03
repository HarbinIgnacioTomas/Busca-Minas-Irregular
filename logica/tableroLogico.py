import random
from logica.celdaLogica import celdaLogica


class tableroLogico:
    def __init__(self, filas, columnas, cant_minas, cant_celdas_irregulares):
        self.filas = filas
        self.columnas = columnas
        self.cant_minas = cant_minas
        self.minas = []
        self.celdas = self.definir_celdas(filas, columnas, cant_celdas_irregulares)
        self.celdas_restantes = len(set(self.celdas.values())) - cant_minas #celdas NO minas que faltan revelar para ganar


    #guarda cada coordenada (key: (fila, columna)) asociada a su celda (objeto) en un diccionario
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

            #guarda las 9 coordenadas necesarias para validar que no se pisen los bloques 2*2
            #y las 4 coordenadas de las celdas 2*2 en el diccionario
            for c in range(columna_rand-1, columna_rand+2):
                for f in range(fila_rand-1, fila_rand+2):
                    celdas_aux.add((f, c))
                    if 0 <= f < filas and 0 <= c < columnas:
                        celdas_aux.add((f, c))
                        if c >= columna_rand and f >= fila_rand:
                            coordenadas.append((f, c))

            #asocia las 4 coordenadas creando un objeto celda
            #y guarda las coordenadas como clave que apuntan a su misma celda
            nueva_celda = celdaLogica(coordenadas)
            for coordenada in coordenadas:
                celdas[coordenada] = nueva_celda

        #guarda en el diccionario todas las celdas 1*1 restantes
        for fila in range(filas):
            for columna in range(columnas):
                if (fila, columna) not in celdas:
                    nueva_celda = celdaLogica([fila, columna])
                    celdas[(fila, columna)] = nueva_celda

        self.definir_vecinos(celdas)

        return celdas

    def definir_vecinos(self, celdas):
        #le asigna a cada celda un set con todas sus celdas vecinas
        #esto evita tener que trabajar con coordenadas al hacer barridos de varias celdas vecinas
        for coordenada, celda in celdas.items():
            fila, columna = coordenada
            for f in range(fila - 1, fila + 2):
                for c in range(columna - 1, columna + 2):
                    if 0 <= f < self.filas and 0 <= c < self.columnas:
                        celda_vecina = celdas[(f, c)]
                        if celda_vecina is not celda:
                        #contempla que la coordenada vecina no forme parte de la misa celda grande
                            celda.vecinas.add(celda_vecina)

    def colocar_minas_y_numeros(self, primera_celda):
        #se encarga de colocar minas en coordenadas aleatorias guardandolas en las celdas en el atributo es_mina
        #valida que las coordenadas no pertenezcan a una celda ya usada, pertenezcan a celdas normales o celdas grandes

        i = 0

        #bloque que asegura que la primera celda revelada este vacia
        primera_celda.celda_segura = True
        for vecina in primera_celda.vecinas:
            vecina.celda_segura = True

        while i < self.cant_minas:
            fila = random.randrange(self.filas)
            columna = random.randrange(self.columnas)

            if not self.celdas[(fila, columna)].es_mina and not self.celdas[(fila, columna)].celda_segura:
                self.celdas[(fila, columna)].es_mina = True
                self.minas.append(self.celdas[(fila, columna)])
                #por cada mina colocada, actualiza los numeros a su alrededor
                self.calcular_numeros(self.celdas[(fila, columna)])
                i += 1

    def calcular_numeros(self, celda_mina):
        #accede a las celdas vecinas de una mina pasada como paramametro
        #y actualiza sus valores
        #se llama por cada mina colocada en colocar_minas_y_numeros
        for vecina in celda_mina.vecinas:
            if not vecina.es_mina:
                if vecina.valor is None:
                    vecina.valor = 0
                vecina.valor += 1

    def celdas_a_mostrar(self, celda):
        #procesa todas las celdas que se deben mostrar luego de un click
        #y las retorna en un set a la clase Juego para que las procese
        celdas_reveladas = set()
        if not celda.oculta:
            return celdas_reveladas
        if celda.valor is not None:
            #le dice a la celda que se "muestre" si es que tiene numero
            celda.oculta = False
            self.celdas_restantes -= 1
            celdas_reveladas.add(celda)
        else:
            #si la celda no tiene numero genera una cascada de celdas a mostrar
            self.cascada(celda, celdas_reveladas)

        return celdas_reveladas

    def cascada(self, celda_actual, celdas_reveladas):
        #metodo recursivo que actualiza por cada celda el estado de oculto segun corresponda
        #y almacena las celdas en un set
        #si una celda es vacia, debe mostrar a todas sus vecinas
        #hasta que no hayan celdas vacias limitando unas con otras
        celda_actual.oculta = False
        self.celdas_restantes -= 1
        celdas_reveladas.add(celda_actual)
        for vecina in celda_actual.vecinas:
            if vecina.oculta:
                if vecina.valor is not None:
                    vecina.oculta = False
                    self.celdas_restantes -= 1
                    celdas_reveladas.add(vecina)
                else:
                    self.cascada(vecina, celdas_reveladas)

    def imprimir_tablero(self, celdas):
        # metodo para comprobar la creacion correcta del tablero y disposicion de minas/valores
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

# tablero = tableroLogicoIrregular(18,14,40,5,5,0)
# tablero.colocar_minas_y_numeros(tablero.celdas)
# tablero.imprimir_tablero(tablero.celdas)