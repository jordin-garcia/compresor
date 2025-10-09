import math
from PyQt6.QtWidgets import QApplication, QFileDialog
from PIL import Image
import sys

def select_img():
    # Crear aplicación temporal si no existe (requerido por PyQt)
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    # Abrir el cuadro de diálogo para seleccionar archivo
    ruta, _ = QFileDialog.getOpenFileName(
        None,  # Ventana padre (None = sin ventana principal)
        "Seleccionar imagen",  # Título del cuadro
        "../public",  # Carpeta inicial
        "Imágenes (*.png *.jpg *.jpeg *.bmp)"  # Filtro de archivos
    )

    # Si se seleccionó una ruta, devolverla
    if ruta:
        return ruta
    else:
        print(" No se seleccionó ninguna imagen.")
        sys.exit()

# ------------------------------
# Cargar imagen seleccionada y convertir a RGB
# ------------------------------
ruta = select_img()

imagen = Image.open(ruta)
imagen = imagen.convert("RGB")

print(f"Imagen cargada correctamente: {ruta}")
print(f"Dimensiones: {imagen.width} × {imagen.height}")

pixeles = [[imagen.getpixel((x, y)) for x in range(imagen.width)] for y in range(imagen.height)]
ancho, alto = imagen.size

# ------------------------------
# Función: aplanar imagen (para RLE global)
# ------------------------------
def aplanar_imagen(imagen):
    return [pixel for fila in imagen for pixel in fila]

# ------------------------------
# Compresión RLE
# ------------------------------
def comprimir_rle(secuencia):
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

# ------------------------------
# Calcular bits con log2
# ------------------------------
def calcular_bits_rle(runs):
    max_run = max(conteo for _, conteo in runs)
    bits_contador = math.ceil(math.log2(max_run + 1))
    bits_totales = len(runs) * (24 + bits_contador)
    return bits_totales, bits_contador, max_run

# ------------------------------
# Descompresion RLE
# ------------------------------
def descomprimir_rle(comprimidos):
    """Reconstruye la secuencia original de píxeles"""
    secuencia = []
    for color, cantidad in comprimidos:
        secuencia.extend([color] * cantidad)
    return secuencia

# ------------------------------
# Compresión GLOBAL
# ------------------------------
print("\nCompresión GLOBAL:")
imagen_aplanada = aplanar_imagen(pixeles)
runs_global = comprimir_rle(imagen_aplanada)
bits_global, bits_c_global, max_run_global = calcular_bits_rle(runs_global)

print(f"Secuencia global (primeros 50): {runs_global[:50]} ...")
print(f"max_run={max_run_global}, bits_contador={bits_c_global}, bits_totales={bits_global}")

# Guardar resultado de compresion
with open("../public/imagen_comprimida.bin", "wb") as f:
    for color, rep in runs_global:
        # Guardar los 3 bytes del color RGB
        f.write(bytes(color))
        # Guardar la cantidad como 2 bytes (big-endian)
        f.write(rep.to_bytes(2, byteorder='big'))


# ------------------------------
# Descompresión y reconstrucción de la imagen
# ------------------------------
pixeles_recuperados = descomprimir_rle(runs_global)

# Verificar que tenga el mismo número de píxeles
assert len(pixeles_recuperados) == ancho * alto, "Error: número de píxeles no coincide."

# Reconstruir matriz de píxeles
matriz_recuperada = [
    pixeles_recuperados[i * ancho:(i + 1) * ancho] for i in range(alto)
]

# Crear imagen nueva
imagen_reconstruida = Image.new("RGB", (ancho, alto))
for y in range(alto):
    for x in range(ancho):
        imagen_reconstruida.putpixel((x, y), matriz_recuperada[y][x])

# Guardar resultado de descompresion (Reconstruyendo la imagen)
imagen_reconstruida.save("../public/imagen_reconstruida.png")
print("Imagen reconstruida guardada como 'iamgen_reconstruida.png'")

# ------------------------------
# Comparar resultados
# ------------------------------
pixeles_totales = len(imagen_aplanada)
print(f"Pixeles totales: {pixeles_totales}")
bits_original = pixeles_totales * 24

print("\nComparación:")
print(f"  Bits originales : {bits_original}")
print(f"  Global          : {bits_global}")
print(f"  Ahorro global   : {100 - (bits_global / bits_original) * 100:.2f}%")
