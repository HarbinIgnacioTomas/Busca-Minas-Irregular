import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from gui.tableroGrafico import TableroGrafico
from logica.juego import Juego, EstadoJuego


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.juego = Juego()

        #instancia el tablero grafico y le da la estructura con datos primitivos para dibujar la grilla
        self.tablero_grafico = TableroGrafico(self.juego.obtener_estructura(), parent=self)

        self.tablero_grafico.coordenadas_celda.connect(self.procesar_click_en_juego)

        self.setCentralWidget(self.tablero_grafico)



        self.init_ui()

    def init_ui(self):
        # Configuraciones básicas de la ventana
        self.setWindowTitle("BuscaMinas")
        self.resize(400, 300)  # Tamaño inicial de prueba

    def procesar_click_en_juego(self, coordenadas):

        celdas_a_mostrar, estado = self.juego.evaluar_movimiento(coordenadas)
        self.tablero_grafico.actualizar_celdas_graficas(celdas_a_mostrar)

        if estado == EstadoJuego.PERDIDO or estado == EstadoJuego.GANADO:
            self.mostrar_resultado(estado)

    def mostrar_resultado(self, resultado):
        #sea cual sea el resultado, se bloquea el tablero
        self.tablero_grafico.bloquear_tablero()

        if resultado == EstadoJuego.PERDIDO:
            QMessageBox.critical(self, "Juego Perdido", "Pisaste una mina")
        else:
            QMessageBox.information(self, "Juego ganado", "Descubriste todas las minas")

        #una vez se cierra la ventana, se reinicia el juego
        self.reiniciar_juego()

    def reiniciar_juego(self):
        #se crea un nuevo tablero desde el juego
        #y se vuelve a instancia el tablero grafico desde 0
        self.juego.reiniciar_juego()

        old_widget = self.centralWidget()
        if old_widget:
            old_widget.deleteLater()

        self.tablero_grafico = TableroGrafico(self.juego.obtener_estructura(), parent=self)

        self.tablero_grafico.coordenadas_celda.connect(self.procesar_click_en_juego)

        self.setCentralWidget(self.tablero_grafico)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec_())