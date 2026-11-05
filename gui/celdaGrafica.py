from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QSizePolicy


class CeldaGrafica(QPushButton):

    coordenadas_clicadas = pyqtSignal(list)

    def __init__(self, coordenadas, parent=None):
        super().__init__(parent)
        #recibe la lista de coordenadas que le corresponde a este componente visual
        #(1 tupla para 1x1, o 4 tuplas para el bloque 2x2)
        self.coordenadas = coordenadas


        self.setMinimumSize(40, 40)
        self.setCheckable(True)
        self.setFlat(True)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.setStyleSheet("""
                      QPushButton {
                          background-color: #E0E0E0;   /* Gris claro base */
                          border: 1px solid #C0C0C0;   /* Borde fino para armar la cuadrícula */
                          border-radius: 6px;          /* Esquinas redondeadas */
                      }
                      QPushButton:hover {
                          background-color: #D6D6D6;   /* Gris un poco más oscuro al pasar el mouse */
                      }
                      QPushButton:disabled {
                          background-color: #d4d4d4;   /* Fondo cuando está desactivada/revelada */
                          color: #000000;
                      }
                  """)

    def mousePressEvent(self, event):
        #evalua qué botón se presionó sobre la celda

        if event.button() == Qt.LeftButton:
            if self.text() == "🚩":
                return
            self.coordenadas_clicadas.emit(self.coordenadas)
            self.setEnabled(False)

        elif event.button() == Qt.RightButton:
            if self.text() == "🚩":
                self.setText("")
                self.setStyleSheet("""
                                    QPushButton {
                                        background-color: #E0E0E0;
                                        border: 1px solid #C0C0C0;
                                        border-radius: 6px;
                                    }
                                    QPushButton:hover {
                                        background-color: #D6D6D6;
                                    }
                                """)
            else:
                self.setText("🚩")
                self.setStyleSheet(
                    "font-weight: bold; font-size: 18px; background-color: #fff9c4; color: #000000; border: 1px solid #fbc02d; border-radius: 6px;"
                )

        super().mousePressEvent(event)

    def es_grande(self):
        return len(self.coordenadas) == 4

    def mostrar_valor(self, valor):
        self.setDown(True)
        self.setEnabled(False)
        if valor == 0:
            texto = ""
            self.setStyleSheet(
                "font-weight: bold; font-size: 18px; background-color: #cccccc; border: 1px solid #bbb; border-radius: 6px;"
            )
        elif valor == "M":
            texto = "💣"
            self.setStyleSheet(
                "font-weight: bold; font-size: 18px; background-color: #f44336; color: #fff; border: 1px solid #999; border-radius: 6px;"
            )
        else:
            texto = str(valor)
            colores = {
                1: "#2196F3",
                2: "#4CAF50",
                3: "#F44336",
                4: "#9C27B0",
                5: "#795548",
                6: "#00BCD4",
                7: "#212121",
                8: "#616161",
                9: "#FF9800",
                10: "#E91E63",
                11: "#8BC34A",
                12: "#673AB7"
            }
            color = colores.get(valor, "#000")
            self.setStyleSheet(
                f"font-weight: bold; font-size: 18px; background-color: #d4d4d4; color: {color}; border: 1px solid #bbb; border-radius: 6px;"
            )
        self.setText(texto)
