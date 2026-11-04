from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGridLayout, QWidget
from gui.celdaGrafica import CeldaGrafica


class TableroGrafico(QWidget):

    coordenadas_celda = pyqtSignal(list) #Variable de clase que almacena las coordenadas de una celda presionada
                                         #para enviarsela a la ventana principal

    def __init__(self, datos_tablero, parent=None):
        super().__init__(parent)

        (self.filas, self.columnas), self.estructura_bloques = datos_tablero
        self.celdas_graficas = {}

        # Inicializa la interfaz del tablero
        self.inicializar_ui()

    def inicializar_ui(self):
        # QGridLayout posiciona las celdas en la grilla
        self.layout_grilla = QGridLayout()

        self.layout_grilla.setContentsMargins(0, 0, 0, 0)  # margen de la grilla a la ventana
        self.layout_grilla.setSpacing(0)  # espacio entre celdas

        self.setLayout(self.layout_grilla)
        self.crear_componentes_visuales()

    def crear_componentes_visuales(self):
        # metodo que recorre la estructura y genera los botones por cada celda
        for bloque in self.estructura_bloques:
            celda_grafica = CeldaGrafica(bloque)
            # conecta manejar_click_celda con cada celdaGrafica (boton)
            # para que escuche la señal al ser presionada
            celda_grafica.coordenadas_clicadas.connect(self.manejar_click_celda)

            for coordenada in bloque:
                self.celdas_graficas[tuple(coordenada)] = celda_grafica

            if celda_grafica.es_grande():
                filas = [coords[0] for coords in bloque]
                columnas = [coords[1] for coords in bloque]

                f_min = min(filas)
                c_min = min(columnas)

                self.layout_grilla.addWidget(celda_grafica, f_min, c_min, 2, 2)
            else:
                f, c = bloque[0]
                self.layout_grilla.addWidget(celda_grafica, f, c, 1, 1)

    def manejar_click_celda(self, coordenadas):
        #escucha cada click hecho en las celdas y recibe sus coordenadas
        self.coordenadas_celda.emit(coordenadas)

    def actualizar_celdas_graficas(self, celdas_a_mostrar):
        """Recibe la lista de tuplas con formato:

        [([(fila, columna)], valor), ...] o bloques 2x2
        """
        for coordenadas, valor in celdas_a_mostrar:
            # Como 'coordenadas_bloque' ya es iterable (una lista de tuplas de coordenadas),
            # recorremos directamente cada coordenada sin bucles anidados extra.
            for coordenada in coordenadas:
                # Buscamos el widget gráfico usando la coordenada como clave exacta
                celda_grafica = self.celdas_graficas.get(tuple(coordenada))

                if celda_grafica:
                    # Le mandamos el valor al widget para que lo dibuje en pantalla
                    celda_grafica.mostrar_valor(valor)

    def bloquear_tablero(self):
        #bloque todas las celdas restantes en caso de ganar o perder
        for celda_grafica in set(self.celdas_graficas.values()):
            celda_grafica.setEnabled(False)