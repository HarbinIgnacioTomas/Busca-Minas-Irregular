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
                    nueva_celda = celdaLogica([(fila, columna)])
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

            celda = self.celdas[(fila, columna)]
            if not celda.es_mina and not celda.celda_segura:
                celda.es_mina = True
                self.minas.append((celda.coordenadas, "M"))
                #por cada mina colocada, actualiza los numeros a su alrededor
                self.calcular_numeros(celda)
                i += 1

    def calcular_numeros(self, celda_mina):
        #accede a las celdas vecinas de una mina pasada como paramametro
        #y actualiza sus valores
        #se llama por cada mina colocada en colocar_minas_y_numeros
        for vecina in celda_mina.vecinas:
            if not vecina.es_mina:
                vecina.aumentar_valor()

    def es_mina(self, celda):
        return celda.es_mina

    def celdas_a_mostrar(self, celda):
        #procesa todas las celdas que se deben mostrar luego de un click
        #y las retorna en un set a la clase Juego para que las procese
        celdas_reveladas = set()
        if not celda.oculta:
            return celdas_reveladas
        if celda.valor is not None:
            #le dice a la celda que se "muestre" si es que tiene numero
            celda.revelar()
            self.celdas_restantes -= 1
            celdas_reveladas.add(celda)
        else:
            #si la celda no tiene numero genera una cascada de celdas a mostrar
            self.cascada(celda, celdas_reveladas)

        return self.formatear_celdas_a_mostrar(celdas_reveladas)

    def cascada(self, celda_actual, celdas_reveladas):
        #metodo recursivo que actualiza por cada celda el estado de oculto segun corresponda
        #y almacena las celdas en un set
        #si una celda es vacia, debe mostrar a todas sus vecinas
        #hasta que no hayan celdas vacias limitando unas con otras
        celda_actual.revelar()
        self.celdas_restantes -= 1
        celdas_reveladas.add(celda_actual)
        for vecina in celda_actual.vecinas:
            if vecina.oculta:
                if vecina.valor is not None:
                    vecina.revelar()
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

    def obtener_estructura_bloques(self):
        # metodo encargado de devolver la estructura del tablero
        # para comunicarlo a la vista con valores primitivos
        # y asi evitar acoplamiento con los objetos del modelo
        bloques = []
        celdas_procesadas = set()
        for celda in self.celdas.values():
            if celda in celdas_procesadas:
                continue
            celdas_procesadas.add(celda)

            # celda.coordenadas ya contiene una tupla de tuplas para 2x2
            # o una tupla simple (f, c) para 1x1
            if celda.es_celda_grande():
                bloques.append(celda.coordenadas)
            else:
                bloques.append(celda.coordenadas)  # Se guarda como tupla de 1 elemento


        return bloques

    def obtener_celda(self, coordenadas):
        #devuelve el objeto celda correspondiente a las coordenadas ennviadas por el Juego
        coordenada = tuple(coordenadas[0])
        return self.celdas.get(coordenada)

    def formatear_celdas_a_mostrar(self, celdas_reveladas):
        #Recibe el set de objetos celdaLogica devuelto por celdas_a_mostrar,
        #y genera una estructura de datos pura (lista de tuplas) que contiene
        #las coordenadas y el valor correspondiente (0 si no hay nada, o el número).
        datos_para_la_vista = []
        for celda in celdas_reveladas:
            # Si el valor es None (espacio vacío sin minas cerca), se asigna 0;
            # de lo contrario, se mantiene el número de minas circundantes.
            valor = 0 if celda.valor is None else celda.valor

            # Se agrega la estructura de coordenadas (sea 1x1 o 2x2) junto a su valor
            datos_para_la_vista.append((celda.coordenadas, valor))

        return datos_para_la_vista

# tablero = tableroLogicoIrregular(18,14,40,5,5,0)
# tablero.colocar_minas_y_numeros(tablero.celdas)
# tablero.imprimir_tablero(tablero.celdas)