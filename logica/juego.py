from enum import Enum
from logica.tableroLogico import tableroLogico

class EstadoJuego(Enum):
    #los valores numericos del enum en este caso se almacenan de cara a la escabilidad
    #considerando librerias que interpreten eventos mediante enteros o mecanismos de persistencia
    PERDIDO = -1
    EN_PROGRESO = 0
    GANADO = 1

class Juego:
    def __init__(self):
        self.tablero = tableroLogico(18, 14, 40, 20) #self.crear_tablero()
        self.primera_celda = True

    def evaluar_movimiento(self, celda):
        #retorna un set con las minas a revelarse y el estado del juego luego del movimiento
        #-1 si perdio (era mina), 1 si gano (no quedan celdas por revelar), 0 si el juego continua
        if self.primera_celda:
            #las minas se colocan luego de asegurar que la primera mina sea vacia
            self.tablero.colocar_minas_y_numeros(celda)
            self.primera_celda = False
        celdas_a_mostrar = set()
        if self.tablero.es_mina(celda):
            #estado = EstadoJuego.PERDIDO
            estado = -1
        else:
            #guarda todas las celdas a mostrarse en un set
            celdas_a_mostrar = self.tablero.celdas_a_mostrar(celda)
            #estado = EstadoJuego.GANADO if self.tablero.celdas_restantes == 0 else EstadoJuego.PERDIDO
            estado = 1 if self.tablero.celdas_restantes == 0 else 0
        return celdas_a_mostrar, estado

    def reiniciar_juego(self):
        self.tablero = tableroLogico(18, 14, 40, 20)
        self.primera_celda = True