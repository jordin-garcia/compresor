import sys
from PyQt6.QtWidgets import QApplication
from src.interfaz_grafica import AplicacionCompresion


def main():
    # Punto de entrada principal de la aplicación
    app = QApplication(sys.argv)
    ventana = AplicacionCompresion()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
