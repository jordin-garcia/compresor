import sys
import os
import shutil
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QFileDialog,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PIL import Image

# Importar módulos de compresión
from src.compresion_texto import comprimir_texto, descomprimir_texto
from src.compresion_audio import CompresorAudioOptimizado


class AplicacionCompresion(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Compresor de Datos")
        self.setGeometry(100, 100, 600, 400)
        self.inicializar_interfaz()

    def inicializar_interfaz(self):
        # Inicializa la interfaz principal con menú de opciones
        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        diseño = QVBoxLayout()
        diseño.setSpacing(20)
        diseño.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Título
        titulo = QLabel("Compresor de Datos")
        titulo.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        diseño.addWidget(titulo)

        subtitulo = QLabel("Selecciona el tipo de archivo a comprimir")
        subtitulo.setFont(QFont("Arial", 12))
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        diseño.addWidget(subtitulo)

        diseño.addSpacing(30)

        # Botones principales
        btn_texto = QPushButton("Comprimir/Descomprimir Texto")
        btn_texto.setFont(QFont("Arial", 14))
        btn_texto.setMinimumHeight(60)
        btn_texto.clicked.connect(self.abrir_ventana_texto)
        diseño.addWidget(btn_texto)

        btn_imagen = QPushButton("Comprimir/Descomprimir Imagen")
        btn_imagen.setFont(QFont("Arial", 14))
        btn_imagen.setMinimumHeight(60)
        btn_imagen.clicked.connect(self.abrir_ventana_imagen)
        diseño.addWidget(btn_imagen)

        btn_audio = QPushButton("Comprimir/Descomprimir Audio")
        btn_audio.setFont(QFont("Arial", 14))
        btn_audio.setMinimumHeight(60)
        btn_audio.clicked.connect(self.abrir_ventana_audio)
        diseño.addWidget(btn_audio)

        diseño.addStretch()

        widget_central.setLayout(diseño)

    def abrir_ventana_texto(self):
        # Abre ventana de compresión de texto
        self.ventana_texto = VentanaCompresionTexto()
        self.ventana_texto.show()

    def abrir_ventana_imagen(self):
        # Abre ventana de compresión de imágenes
        self.ventana_imagen = VentanaCompresionImagen()
        self.ventana_imagen.show()

    def abrir_ventana_audio(self):
        # Abre ventana de compresión de audio
        self.ventana_audio = VentanaCompresionAudio()
        self.ventana_audio.show()


class VentanaCompresionTexto(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Compresión de Texto - Huffman")
        self.setGeometry(150, 150, 600, 500)
        self.ruta_archivo = None
        self.inicializar_interfaz()

    def inicializar_interfaz(self):
        diseño = QVBoxLayout()
        diseño.setSpacing(15)

        # Título
        titulo = QLabel("Compresión de Texto (Huffman)")
        titulo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        diseño.addWidget(titulo)

        diseño.addSpacing(20)

        # Sección de compresión
        etiqueta_comprimir = QLabel("COMPRIMIR")
        etiqueta_comprimir.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        diseño.addWidget(etiqueta_comprimir)

        btn_seleccionar = QPushButton("Seleccionar archivo .txt")
        btn_seleccionar.clicked.connect(self.seleccionar_archivo_texto)
        diseño.addWidget(btn_seleccionar)

        self.etiqueta_archivo = QLabel("Ningún archivo seleccionado")
        self.etiqueta_archivo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        diseño.addWidget(self.etiqueta_archivo)

        btn_comprimir = QPushButton("Comprimir")
        btn_comprimir.setMinimumHeight(40)
        btn_comprimir.clicked.connect(self.comprimir_texto_metodo)
        diseño.addWidget(btn_comprimir)

        self.etiqueta_resultado = QLabel("")
        self.etiqueta_resultado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.etiqueta_resultado.setWordWrap(True)
        diseño.addWidget(self.etiqueta_resultado)

        diseño.addSpacing(20)

        # Sección de descompresión
        etiqueta_descomprimir = QLabel("DESCOMPRIMIR")
        etiqueta_descomprimir.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        diseño.addWidget(etiqueta_descomprimir)

        btn_descomprimir = QPushButton("Seleccionar y Descomprimir archivo .bin")
        btn_descomprimir.setMinimumHeight(40)
        btn_descomprimir.clicked.connect(self.descomprimir_texto_metodo)
        diseño.addWidget(btn_descomprimir)

        self.etiqueta_resultado_descompresion = QLabel("")
        self.etiqueta_resultado_descompresion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.etiqueta_resultado_descompresion.setWordWrap(True)
        diseño.addWidget(self.etiqueta_resultado_descompresion)

        diseño.addStretch()

        # Botón volver
        btn_volver = QPushButton("Cerrar")
        btn_volver.clicked.connect(self.close)
        diseño.addWidget(btn_volver)

        self.setLayout(diseño)

    def seleccionar_archivo_texto(self):
        # Selecciona archivo de texto
        # Directorio por defecto: archivos/originales
        directorio_predeterminado = os.path.join(os.getcwd(), "archivos", "originales")
        ruta_archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo de texto",
            directorio_predeterminado,
            "Archivos de texto (*.txt)",
        )
        if ruta_archivo:
            self.ruta_archivo = ruta_archivo
            self.etiqueta_archivo.setText(f"Archivo: {os.path.basename(ruta_archivo)}")

    def comprimir_texto_metodo(self):
        # Comprime el archivo de texto seleccionado
        if not self.ruta_archivo:
            QMessageBox.warning(
                self, "Advertencia", "Por favor selecciona un archivo primero"
            )
            return

        try:
            # Leer el archivo
            with open(self.ruta_archivo, "r", encoding="utf-8") as f:
                texto = f.read()

            if not texto:
                QMessageBox.warning(self, "Advertencia", "El archivo está vacío")
                return

            # Crear carpeta comprimidos si no existe
            directorio_comprimidos = os.path.join(
                os.getcwd(), "archivos", "comprimidos"
            )
            os.makedirs(directorio_comprimidos, exist_ok=True)

            # Crear nombre de archivo comprimido en la carpeta correcta
            nombre_base = os.path.splitext(os.path.basename(self.ruta_archivo))[0]
            archivo_salida = os.path.join(
                directorio_comprimidos, nombre_base + "_comprimido.bin"
            )

            # Comprimir
            comprimir_texto(texto, archivo_salida)

            # Calcular estadísticas
            tamaño_original = os.path.getsize(self.ruta_archivo)
            tamaño_comprimido = os.path.getsize(archivo_salida)
            ratio = tamaño_original / tamaño_comprimido if tamaño_comprimido > 0 else 0
            ahorro_porcentaje = (
                100 * (1 - tamaño_comprimido / tamaño_original)
                if tamaño_original > 0
                else 0
            )

            texto_resultado = "Compresión exitosa!\n"
            texto_resultado += f"Tamaño original: {tamaño_original:,} bytes ({tamaño_original / 1024:.2f} KB)\n"
            texto_resultado += f"Tamaño comprimido: {tamaño_comprimido:,} bytes ({tamaño_comprimido / 1024:.2f} KB)\n"
            texto_resultado += f"Ratio de compresión: {ratio:.2f}:1\n"
            texto_resultado += f"Porcentaje de reducción: {ahorro_porcentaje:.1f}%\n"
            texto_resultado += f"Archivo guardado en: archivos/comprimidos/{os.path.basename(archivo_salida)}"

            self.etiqueta_resultado.setText(texto_resultado)

            # Mensaje informativo
            if ahorro_porcentaje > 0:
                mensaje = "Texto comprimido exitosamente.\n\n"
                mensaje += f"Huffman ahorra {ahorro_porcentaje:.1f}% de espacio de almacenamiento.\n"
            else:
                mensaje = "Texto comprimido (sin reducción de tamaño).\n\n"
                mensaje += (
                    "Este texto tiene mucha variación de caracteres o es muy corto.\n"
                )
                mensaje += "Huffman funciona mejor con texto más uniforme y largo."

            QMessageBox.information(self, "Éxito", mensaje)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al comprimir: {str(e)}")

    def descomprimir_texto_metodo(self):
        # Descomprime un archivo .bin
        # Directorio por defecto: archivos/comprimidos
        directorio_predeterminado = os.path.join(os.getcwd(), "archivos", "comprimidos")
        ruta_archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo comprimido",
            directorio_predeterminado,
            "Archivos binarios (*.bin)",
        )

        if not ruta_archivo:
            return

        try:
            # Crear carpeta descomprimidos si no existe
            directorio_descomprimidos = os.path.join(
                os.getcwd(), "archivos", "descomprimidos"
            )
            os.makedirs(directorio_descomprimidos, exist_ok=True)

            # Crear nombre de archivo de salida en la carpeta correcta
            nombre_base = os.path.splitext(os.path.basename(ruta_archivo))[0]
            # Remover "_comprimido" si está en el nombre
            if nombre_base.endswith("_comprimido"):
                nombre_base = nombre_base[:-11]
            archivo_salida = os.path.join(
                directorio_descomprimidos, nombre_base + "_descomprimido.txt"
            )

            # Descomprimir
            texto = descomprimir_texto(ruta_archivo, archivo_salida)

            texto_resultado = "Descompresión exitosa!\n"
            texto_resultado += f"Archivo guardado en: archivos/descomprimidos/{os.path.basename(archivo_salida)}\n"
            texto_resultado += f"Caracteres recuperados: {len(texto)}"

            self.etiqueta_resultado_descompresion.setText(texto_resultado)
            QMessageBox.information(self, "Éxito", "Texto descomprimido exitosamente")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al descomprimir: {str(e)}")


class VentanaCompresionImagen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Compresión de Imágenes - RLE")
        self.setGeometry(150, 150, 600, 500)
        self.ruta_archivo = None
        self.inicializar_interfaz()

    def inicializar_interfaz(self):
        diseño = QVBoxLayout()
        diseño.setSpacing(15)

        # Título
        titulo = QLabel("Compresión de Imágenes (RLE)")
        titulo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        diseño.addWidget(titulo)

        diseño.addSpacing(20)

        # Sección de compresión
        etiqueta_comprimir = QLabel("COMPRIMIR")
        etiqueta_comprimir.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        diseño.addWidget(etiqueta_comprimir)

        btn_seleccionar = QPushButton("Seleccionar imagen")
        btn_seleccionar.clicked.connect(self.seleccionar_archivo_imagen)
        diseño.addWidget(btn_seleccionar)

        self.etiqueta_archivo = QLabel("Ningún archivo seleccionado")
        self.etiqueta_archivo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        diseño.addWidget(self.etiqueta_archivo)

        btn_comprimir = QPushButton("Comprimir")
        btn_comprimir.setMinimumHeight(40)
        btn_comprimir.clicked.connect(self.comprimir_imagen_metodo)
        diseño.addWidget(btn_comprimir)

        self.etiqueta_resultado = QLabel("")
        self.etiqueta_resultado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.etiqueta_resultado.setWordWrap(True)
        diseño.addWidget(self.etiqueta_resultado)

        diseño.addSpacing(20)

        # Sección de descompresión
        etiqueta_descomprimir = QLabel("DESCOMPRIMIR")
        etiqueta_descomprimir.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        diseño.addWidget(etiqueta_descomprimir)

        btn_descomprimir = QPushButton("Seleccionar y Descomprimir archivo .bin")
        btn_descomprimir.setMinimumHeight(40)
        btn_descomprimir.clicked.connect(self.descomprimir_imagen_metodo)
        diseño.addWidget(btn_descomprimir)

        self.etiqueta_resultado_descompresion = QLabel("")
        self.etiqueta_resultado_descompresion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.etiqueta_resultado_descompresion.setWordWrap(True)
        diseño.addWidget(self.etiqueta_resultado_descompresion)

        diseño.addStretch()

        # Botón volver
        btn_volver = QPushButton("Cerrar")
        btn_volver.clicked.connect(self.close)
        diseño.addWidget(btn_volver)

        self.setLayout(diseño)

    def seleccionar_archivo_imagen(self):
        # Selecciona archivo de imagen
        # Directorio por defecto: archivos/originales
        directorio_predeterminado = os.path.join(os.getcwd(), "archivos", "originales")
        ruta_archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar imagen",
            directorio_predeterminado,
            "Imágenes (*.png *.jpg *.jpeg *.bmp)",
        )
        if ruta_archivo:
            self.ruta_archivo = ruta_archivo
            self.etiqueta_archivo.setText(f"Archivo: {os.path.basename(ruta_archivo)}")

    def aplanar_imagen(self, imagen):
        # Aplana matriz de imagen
        return [pixel for fila in imagen for pixel in fila]

    def comprimir_rle(self, secuencia):
        # Compresión RLE
        comprimidos = []
        actual = secuencia[0]
        conteo = 1
        for pixel in secuencia[1:]:
            if pixel == actual:
                conteo += 1
            else:
                comprimidos.append((actual, conteo))
                actual = pixel
                conteo = 1
        comprimidos.append((actual, conteo))
        return comprimidos

    def descomprimir_rle(self, comprimidos):
        # Descompresión RLE
        secuencia = []
        for color, cantidad in comprimidos:
            secuencia.extend([color] * cantidad)
        return secuencia

    def comprimir_imagen_metodo(self):
        # Comprime la imagen seleccionada
        if not self.ruta_archivo:
            QMessageBox.warning(
                self, "Advertencia", "Por favor selecciona una imagen primero"
            )
            return

        try:
            # Cargar y convertir imagen
            imagen = Image.open(self.ruta_archivo)
            imagen = imagen.convert("RGB")

            ancho, alto = imagen.size
            pixeles = [
                [imagen.getpixel((x, y)) for x in range(ancho)] for y in range(alto)
            ]

            # Comprimir
            imagen_aplanada = self.aplanar_imagen(pixeles)
            ejecuciones_globales = self.comprimir_rle(imagen_aplanada)

            # Crear carpeta comprimidos si no existe
            directorio_comprimidos = os.path.join(
                os.getcwd(), "archivos", "comprimidos"
            )
            os.makedirs(directorio_comprimidos, exist_ok=True)

            # Crear nombre de archivo comprimido en la carpeta correcta
            nombre_base = os.path.splitext(os.path.basename(self.ruta_archivo))[0]
            archivo_salida = os.path.join(
                directorio_comprimidos, nombre_base + "_comprimido.bin"
            )

            # Guardar
            with open(archivo_salida, "wb") as f:
                # Guardar dimensiones primero
                f.write(ancho.to_bytes(4, byteorder="big"))
                f.write(alto.to_bytes(4, byteorder="big"))
                # Guardar datos RLE
                for color, rep in ejecuciones_globales:
                    f.write(bytes(color))
                    f.write(rep.to_bytes(2, byteorder="big"))

            # Calcular estadísticas CORRECTAMENTE
            tamaño_raw = ancho * alto * 3  # Tamaño sin comprimir (RAW RGB)
            tamaño_png = os.path.getsize(
                self.ruta_archivo
            )  # Tamaño del PNG/JPG original
            tamaño_comprimido = os.path.getsize(archivo_salida)  # Tamaño RLE comprimido
            ratio = tamaño_raw / tamaño_comprimido if tamaño_comprimido > 0 else 0
            ahorro_porcentaje = (
                100 * (1 - tamaño_comprimido / tamaño_raw) if tamaño_raw > 0 else 0
            )

            texto_resultado = "Compresión exitosa!\n"
            texto_resultado += f"Dimensiones: {ancho} × {alto}\n"
            texto_resultado += "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            texto_resultado += f"Tamaño RAW (sin comprimir): {tamaño_raw:,} bytes ({tamaño_raw / 1024:.2f} KB)\n"
            texto_resultado += f"Tamaño PNG/JPG original: {tamaño_png:,} bytes ({tamaño_png / 1024:.2f} KB)\n"
            texto_resultado += f"Tamaño RLE comprimido: {tamaño_comprimido:,} bytes ({tamaño_comprimido / 1024:.2f} KB)\n"
            texto_resultado += "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            texto_resultado += f"Ratio compresión (vs RAW): {ratio:.2f}:1\n"
            texto_resultado += f"Porcentaje de reducción (Comprimido vs RAW): {ahorro_porcentaje:.1f}%\n"
            texto_resultado += "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            texto_resultado += f"Archivo guardado en: archivos/comprimidos/{os.path.basename(archivo_salida)}"

            self.etiqueta_resultado.setText(texto_resultado)

            # Mensaje informativo
            if ahorro_porcentaje > 0:
                mensaje = "Imagen comprimida exitosamente.\n\n"
                mensaje += f"RLE ahorra {ahorro_porcentaje:.1f}% de espacio de almacenamiento.\n"
            else:
                mensaje = "Imagen comprimida (sin reducción de tamaño).\n\n"
                mensaje += "Este imagen tiene mucha variación de colores.\n"
                mensaje += "RLE funciona mejor con imágenes más uniformes."

            QMessageBox.information(self, "Éxito", mensaje)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al comprimir: {str(e)}")

    def descomprimir_imagen_metodo(self):
        # Descomprime una imagen .bin
        # Directorio por defecto: archivos/comprimidos
        directorio_predeterminado = os.path.join(os.getcwd(), "archivos", "comprimidos")
        ruta_archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo comprimido",
            directorio_predeterminado,
            "Archivos binarios (*.bin)",
        )

        if not ruta_archivo:
            return

        try:
            # Leer archivo comprimido
            with open(ruta_archivo, "rb") as f:
                # Leer dimensiones
                ancho = int.from_bytes(f.read(4), byteorder="big")
                alto = int.from_bytes(f.read(4), byteorder="big")

                # Leer datos RLE
                ejecuciones = []
                while True:
                    bytes_color = f.read(3)
                    if not bytes_color or len(bytes_color) < 3:
                        break
                    bytes_rep = f.read(2)
                    if not bytes_rep or len(bytes_rep) < 2:
                        break
                    color = tuple(bytes_color)
                    rep = int.from_bytes(bytes_rep, byteorder="big")
                    ejecuciones.append((color, rep))

            # Descomprimir
            pixeles_recuperados = self.descomprimir_rle(ejecuciones)

            # Reconstruir imagen
            matriz_recuperada = [
                pixeles_recuperados[i * ancho : (i + 1) * ancho] for i in range(alto)
            ]

            imagen_reconstruida = Image.new("RGB", (ancho, alto))
            for y in range(alto):
                for x in range(ancho):
                    imagen_reconstruida.putpixel((x, y), matriz_recuperada[y][x])

            # Crear carpeta descomprimidos si no existe
            directorio_descomprimidos = os.path.join(
                os.getcwd(), "archivos", "descomprimidos"
            )
            os.makedirs(directorio_descomprimidos, exist_ok=True)

            # Guardar en la carpeta correcta
            nombre_base = os.path.splitext(os.path.basename(ruta_archivo))[0]
            # Remover "_comprimido" si está en el nombre
            if nombre_base.endswith("_comprimido"):
                nombre_base = nombre_base[:-11]
            archivo_salida = os.path.join(
                directorio_descomprimidos, nombre_base + "_descomprimido.png"
            )
            imagen_reconstruida.save(archivo_salida)

            texto_resultado = "Descompresión exitosa!\n"
            texto_resultado += f"Dimensiones: {ancho} × {alto}\n"
            texto_resultado += f"Archivo guardado en: archivos/descomprimidos/{os.path.basename(archivo_salida)}"

            self.etiqueta_resultado_descompresion.setText(texto_resultado)
            QMessageBox.information(self, "Éxito", "Imagen descomprimida exitosamente")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al descomprimir: {str(e)}")


class VentanaCompresionAudio(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Compresión de Audio - RLE + Huffman")
        self.setGeometry(150, 150, 600, 500)
        self.ruta_archivo = None
        self.compresor = CompresorAudioOptimizado()
        self.inicializar_interfaz()

    def inicializar_interfaz(self):
        diseño = QVBoxLayout()
        diseño.setSpacing(15)

        # Título
        titulo = QLabel("Compresión de Audio (RLE + Huffman)")
        titulo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        diseño.addWidget(titulo)

        diseño.addSpacing(20)

        # Sección de compresión
        etiqueta_comprimir = QLabel("COMPRIMIR")
        etiqueta_comprimir.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        diseño.addWidget(etiqueta_comprimir)

        btn_seleccionar = QPushButton("Seleccionar archivo .wav")
        btn_seleccionar.clicked.connect(self.seleccionar_archivo_audio)
        diseño.addWidget(btn_seleccionar)

        self.etiqueta_archivo = QLabel("Ningún archivo seleccionado")
        self.etiqueta_archivo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        diseño.addWidget(self.etiqueta_archivo)

        btn_comprimir = QPushButton("Comprimir")
        btn_comprimir.setMinimumHeight(40)
        btn_comprimir.clicked.connect(self.comprimir_audio_metodo)
        diseño.addWidget(btn_comprimir)

        self.etiqueta_resultado = QLabel("")
        self.etiqueta_resultado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.etiqueta_resultado.setWordWrap(True)
        diseño.addWidget(self.etiqueta_resultado)

        diseño.addSpacing(20)

        # Sección de descompresión
        etiqueta_descomprimir = QLabel("DESCOMPRIMIR")
        etiqueta_descomprimir.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        diseño.addWidget(etiqueta_descomprimir)

        btn_descomprimir = QPushButton("Seleccionar y Descomprimir archivo .hac")
        btn_descomprimir.setMinimumHeight(40)
        btn_descomprimir.clicked.connect(self.descomprimir_audio_metodo)
        diseño.addWidget(btn_descomprimir)

        self.etiqueta_resultado_descompresion = QLabel("")
        self.etiqueta_resultado_descompresion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.etiqueta_resultado_descompresion.setWordWrap(True)
        diseño.addWidget(self.etiqueta_resultado_descompresion)

        diseño.addSpacing(10)

        # Botón reproducir
        btn_reproducir = QPushButton("Reproducir último archivo descomprimido")
        btn_reproducir.clicked.connect(self.reproducir_audio_metodo)
        diseño.addWidget(btn_reproducir)

        # Botón detener reproducción
        btn_detener = QPushButton("Detener Reproducción")
        btn_detener.clicked.connect(self.detener_reproduccion_metodo)
        diseño.addWidget(btn_detener)

        diseño.addStretch()

        # Botón volver
        btn_volver = QPushButton("Cerrar")
        btn_volver.clicked.connect(self.close)
        diseño.addWidget(btn_volver)

        self.setLayout(diseño)

    def seleccionar_archivo_audio(self):
        # Selecciona archivo de audio
        # Directorio por defecto: archivos/originales
        directorio_predeterminado = os.path.join(os.getcwd(), "archivos", "originales")
        ruta_archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo de audio",
            directorio_predeterminado,
            "Archivos WAV (*.wav)",
        )
        if ruta_archivo:
            self.ruta_archivo = ruta_archivo
            self.etiqueta_archivo.setText(f"Archivo: {os.path.basename(ruta_archivo)}")

    def comprimir_audio_metodo(self):
        # Comprime el archivo de audio seleccionado
        if not self.ruta_archivo:
            QMessageBox.warning(
                self, "Advertencia", "Por favor selecciona un archivo primero"
            )
            return

        try:
            # Leer información del archivo WAV primero para obtener tamaño RAW
            import wave

            with wave.open(self.ruta_archivo, "rb") as wav:
                num_frames = wav.getnframes()
                ancho_muestra = wav.getsampwidth()
                canales = wav.getnchannels()

            # Tamaño RAW de audio (datos PCM sin comprimir, sin headers WAV)
            tamaño_raw = num_frames * ancho_muestra * canales

            # Comprimir (el módulo crea el archivo en la misma carpeta que el original)
            resultado = self.compresor.comprimir_audio(self.ruta_archivo)

            if resultado:
                # El archivo comprimido se crea junto al original
                nombre_base = os.path.splitext(self.ruta_archivo)[0]
                archivo_salida_temporal = nombre_base + "_comprimido.hac"

                # Crear carpeta comprimidos si no existe
                directorio_comprimidos = os.path.join(
                    os.getcwd(), "archivos", "comprimidos"
                )
                os.makedirs(directorio_comprimidos, exist_ok=True)

                # Mover el archivo a la carpeta correcta
                archivo_salida_final = os.path.join(
                    directorio_comprimidos, os.path.basename(archivo_salida_temporal)
                )
                shutil.move(archivo_salida_temporal, archivo_salida_final)

                # Calcular estadísticas CORRECTAMENTE
                tamaño_wav = os.path.getsize(self.ruta_archivo)  # WAV con headers
                tamaño_comprimido = os.path.getsize(
                    archivo_salida_final
                )  # HAC comprimido
                ratio = tamaño_raw / tamaño_comprimido if tamaño_comprimido > 0 else 0
                ahorro_porcentaje = (
                    100 * (1 - tamaño_comprimido / tamaño_raw) if tamaño_raw > 0 else 0
                )

                texto_resultado = "Compresión exitosa!\n"
                texto_resultado += "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                texto_resultado += f"Tamaño RAW (datos PCM): {tamaño_raw:,} bytes ({tamaño_raw / 1024:.2f} KB)\n"
                texto_resultado += f"Tamaño WAV original: {tamaño_wav:,} bytes ({tamaño_wav / 1024:.2f} KB)\n"
                texto_resultado += f"Tamaño HAC comprimido: {tamaño_comprimido:,} bytes ({tamaño_comprimido / 1024:.2f} KB)\n"
                texto_resultado += "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                texto_resultado += f"Ratio compresión (vs RAW): {ratio:.2f}:1\n"
                texto_resultado += f"Porcentaje de reducción (Comprimido vs RAW): {ahorro_porcentaje:.1f}%\n"
                texto_resultado += "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                texto_resultado += f"Archivo guardado en: archivos/comprimidos/{os.path.basename(archivo_salida_final)}"

                self.etiqueta_resultado.setText(texto_resultado)

                # Mensaje informativo
                if ahorro_porcentaje > 0:
                    mensaje = "Audio comprimido exitosamente.\n\n"
                    mensaje += f"RLE+Huffman ahorra {ahorro_porcentaje:.1f}% de espacio de almacenamiento.\n"
                else:
                    mensaje = "Audio comprimido (sin reducción de tamaño).\n\n"
                    mensaje += "Este audio tiene mucha variación o es muy corto.\n"
                    mensaje += "El overhead del árbol Huffman es mayor que el ahorro.\n"
                    mensaje += (
                        "RLE+Huffman funciona mejor con audio más uniforme y largo."
                    )

                QMessageBox.information(self, "Éxito", mensaje)
            else:
                QMessageBox.critical(self, "Error", "Error al comprimir el audio")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al comprimir: {str(e)}")

    def descomprimir_audio_metodo(self):
        # Descomprime un archivo .hac
        # Directorio por defecto: archivos/comprimidos
        directorio_predeterminado = os.path.join(os.getcwd(), "archivos", "comprimidos")
        ruta_archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo comprimido",
            directorio_predeterminado,
            "Archivos HAC (*.hac)",
        )

        if not ruta_archivo:
            return

        try:
            # Descomprimir (el módulo crea el archivo en la misma carpeta que el comprimido)
            archivo_salida_temporal = self.compresor.descomprimir_audio(ruta_archivo)

            if archivo_salida_temporal:
                # Crear carpeta descomprimidos si no existe
                directorio_descomprimidos = os.path.join(
                    os.getcwd(), "archivos", "descomprimidos"
                )
                os.makedirs(directorio_descomprimidos, exist_ok=True)

                # Mover el archivo a la carpeta correcta
                archivo_salida_final = os.path.join(
                    directorio_descomprimidos, os.path.basename(archivo_salida_temporal)
                )
                shutil.move(archivo_salida_temporal, archivo_salida_final)

                self.ultimo_descomprimido = archivo_salida_final

                texto_resultado = "Descompresión exitosa!\n"
                texto_resultado += f"Archivo guardado en: archivos/descomprimidos/{os.path.basename(archivo_salida_final)}"

                self.etiqueta_resultado_descompresion.setText(texto_resultado)
                QMessageBox.information(
                    self, "Éxito", "Audio descomprimido exitosamente"
                )
            else:
                QMessageBox.critical(self, "Error", "Error al descomprimir el audio")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al descomprimir: {str(e)}")

    def reproducir_audio_metodo(self):
        # Reproduce el último archivo descomprimido
        if hasattr(self, "ultimo_descomprimido"):
            try:
                self.compresor.reproducir_audio(self.ultimo_descomprimido)
                QMessageBox.information(self, "Reproducción", "Reproduciendo audio...")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al reproducir: {str(e)}")
        else:
            QMessageBox.warning(
                self, "Advertencia", "Primero descomprime un archivo de audio"
            )

    def detener_reproduccion_metodo(self):
        # Detiene la reproducción de audio
        try:
            if self.compresor.esta_reproduciendo():
                self.compresor.detener_reproduccion()
                QMessageBox.information(self, "Detener", "Reproducción detenida")
            else:
                QMessageBox.information(
                    self, "Información", "No hay reproducción en curso"
                )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al detener: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = AplicacionCompresion()
    ventana.show()
    sys.exit(app.exec())
