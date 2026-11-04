from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QSizePolicy


class CeldaGrafica(QPushButton):

    coordenadas_clicadas = pyqtSignal(list)

    def __init__(self, coordenadas, parent=None):
        super().__init__(parent)
        # Recibe la lista de coordenadas que le corresponde a este componente visual
        # (1 tupla para 1x1, o 4 tuplas para el bloque 2x2)
        self.coordenadas = coordenadas

        # Configuraciones visuales iniciales
        self.setMinimumSize(40, 40)
        self.setCheckable(True)  # Útil si querés que quede presionada visualmente

        # --- CAMBIOS ESTÉTICOS ---
        self.setFlat(True)  # Elimina el relieve 3D nativo del sistema operativo
        self.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Preferred
        )  # Asegura una correcta distribución en la grilla

        # Estilo visual unificado (fondo gris claro, bordes finos y rectos)
        self.setStyleSheet("""
              QPushButton {
                  background-color: #E0E0E0;   /* Gris claro base */
                  border: 1px solid #C0C0C0;   /* Borde fino para armar la cuadrícula */
                  border-radius: 0px;          /* Cero radio para evitar esquinas redondeadas */
              }
              QPushButton:hover {
                  background-color: #D6D6D6;   /* Gris un poco más oscuro al pasar el mouse */
              }
              QPushButton:checked {
                  background-color: #CCCCCC;   /* Color cuando queda presionada/revelada */
              }
          """)

    def mousePressEvent(self, event):
        # Evaluamos qué botón del mouse presionó el usuario
        if event.button() == Qt.LeftButton:
            if self.text() == "B":
                return
            self.coordenadas_clicadas.emit(self.coordenadas)
            self.setEnabled(False)


        elif event.button() == Qt.RightButton:
            if self.text() == "B":
                self.setText("")
            else:
                self.setText("B")

        # Llamamos al evento original para que el botón no pierda su comportamiento visual base
        super().mousePressEvent(event)

    def es_grande(self):
        return len(self.coordenadas) == 4

    def mostrar_valor(self, valor):
        self.setDown(True)
        self.setEnabled(False)
        if valor == 0:
            texto = ""
        elif valor == "M":
            texto = "x"
        else:
            texto = str(valor)
        self.setText(texto)
