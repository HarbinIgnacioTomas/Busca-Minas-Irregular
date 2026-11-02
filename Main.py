import sys
from PyQt5.QtWidgets import QApplication
from gui.ventanaPrincipal import MainWindow


def main():
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()