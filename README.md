# Compresor de Datos

Aplicación de compresión de datos que implementa algoritmos de compresión sin pérdida para texto, imágenes y audio utilizando Python y PyQt6.

## Integrantes del Equipo

- **Elizabeth Caxaj - 2016523**: Compresión de Audio (RLE + Huffman)
- **Cristian Guzman - 1522919**: Compresión de Imágenes (RLE)
- **André Velasco - 1546124**: Compresión de Texto (Huffman)
- **Jordin García - 2427124**: Interfaz Gráfica (PyQt6)

## Descripción

Este proyecto implementa tres tipos de compresión de datos sin pérdida:

### 1. Compresión de Texto - Algoritmo de Huffman

- Utiliza codificación de Huffman para comprimir archivos de texto
- Genera un árbol binario basado en la frecuencia de caracteres
- Asigna códigos binarios más cortos a caracteres más frecuentes
- Formato de salida: `.bin`

### 2. Compresión de Imágenes - Run-Length Encoding (RLE)

- Comprime imágenes identificando secuencias de píxeles repetidos
- Funciona especialmente bien con imágenes que tienen áreas de color uniforme
- Preserva la calidad original (compresión sin pérdida)
- Formatos soportados: PNG, JPG, JPEG, BMP
- Formato de salida: `.bin`

### 3. Compresión de Audio - RLE + Huffman

- Combina dos algoritmos para máxima eficiencia:
  - Primero aplica RLE para reducir redundancia
  - Luego aplica Huffman para codificación óptima
- Incluye funcionalidad de reproducción de audio
- Formato soportado: WAV
- Formato de salida: `.hac`

## Requisitos del Sistema

- Python 3.8 o superior
- Sistema operativo: Windows, macOS o Linux

## Instalación

### 1. Clonar el repositorio

```bash
git clone [URL_DEL_REPOSITORIO]
cd compresor
```

### 2. Instalar dependencias

#### En Windows:

```bash
pip install -r requirements.txt
```

**Nota importante para PyAudio en Windows:**
Si `pip install pyaudio` falla, usa:

```bash
pip install pipwin
pipwin install pyaudio
```

#### En macOS:

```bash
pip install -r requirements.txt
```

#### En Linux (Ubuntu/Debian):

```bash
sudo apt-get install python3-pyaudio portaudio19-dev
pip install -r requirements.txt
```

## Uso

### Ejecutar la aplicación

```bash
python main.py
```

### Interfaz Gráfica

La aplicación presenta un menú principal con tres opciones:

1. **Comprimir/Descomprimir Texto**

   - Selecciona un archivo `.txt` desde `archivos/originales/`
   - Genera un archivo `.bin` comprimido en `archivos/comprimidos/`
   - Descomprime archivos `.bin` de vuelta a `.txt` en `archivos/descomprimidos/`
   - Muestra estadísticas detalladas de compresión
2. **Comprimir/Descomprimir Imagen**

   - Selecciona una imagen (PNG, JPG, BMP) desde `archivos/originales/`
   - Genera un archivo `.bin` comprimido en `archivos/comprimidos/`
   - Reconstruye la imagen desde el archivo comprimido en `archivos/descomprimidos/`
   - Muestra ratio de compresión comparando tamaño RAW vs comprimido
3. **Comprimir/Descomprimir Audio**

   - Selecciona un archivo `.wav` desde `archivos/originales/`
   - Genera un archivo `.hac` comprimido en `archivos/comprimidos/`
   - Descomprime archivos `.hac` de vuelta a `.wav` en `archivos/descomprimidos/`
   - Incluye opción para reproducir el audio descomprimido
   - **Nuevo:** Botón para detener la reproducción en cualquier momento

## Estructura del Proyecto

```
compresor/
│
├── main.py                      # Punto de entrada principal
├── README.md                    # Este archivo
├── requirements.txt             # Dependencias del proyecto
├── plan.md                      # Documentación del plan de desarrollo
│
├── src/
│   ├── compresion_texto.py     # Módulo de compresión de texto (Huffman)
│   ├── compresion_imagen.py    # Módulo de compresión de imágenes (RLE)
│   ├── compresion_audio.py     # Módulo de compresión de audio (RLE + Huffman)
│   └── interfaz_grafica.py     # Interfaz gráfica con PyQt6 (en español)
│
├── archivos/   
│   ├── originales/             # Coloca aquí tus archivos originales para comprimir
│   ├── comprimidos/            # Los archivos comprimidos se guardan aquí
│   ├── descomprimidos/         # Los archivos descomprimidos se guardan aquí
```

### Organización de Archivos

La aplicación organiza automáticamente los archivos en carpetas específicas:

- **`archivos/originales/`**: Directorio predeterminado al seleccionar archivos a comprimir
- **`archivos/comprimidos/`**: Todos los archivos comprimidos (.bin, .hac) se guardan aquí
- **`archivos/descomprimidos/`**: Todos los archivos descomprimidos se guardan aquí

**Nota:** Estas carpetas se crean automáticamente si no existen.

## Dependencias

- **Pillow**: Procesamiento de imágenes
- **NumPy**: Operaciones numéricas optimizadas
- **PyAudio**: Reproducción de audio
- **PyQt6**: Interfaz gráfica de usuario

## Algoritmos Implementados

### Huffman Coding

- Algoritmo de compresión basado en frecuencias
- Genera códigos de longitud variable
- Óptimo para compresión de texto

### Run-Length Encoding (RLE)

- Comprime secuencias repetidas
- Eficiente para datos con alta redundancia
- Simple y rápido

### Combinación RLE + Huffman

- Primero reduce redundancia con RLE
- Luego optimiza con Huffman
- Especialmente efectivo para audio

## Características Técnicas

- ✅ Compresión sin pérdida (lossless)
- ✅ Interfaz gráfica intuitiva completamente en español
- ✅ Cálculo automático de ratios de compresión (comparación RAW vs comprimido)
- ✅ Manejo robusto de errores con mensajes descriptivos
- ✅ Reproducción de audio integrada con control de detención
- ✅ Soporte para múltiples formatos (TXT, PNG, JPG, BMP, WAV)
- ✅ Organización automática de archivos en carpetas dedicadas
- ✅ Estadísticas detalladas de compresión en tiempo real
- ✅ Código optimizado y limpio

## Ejemplos de Uso

### Preparación inicial

1. Crea la carpeta `archivos/originales/` si no existe
2. Coloca tus archivos de prueba (txt, imágenes, wav) en `archivos/originales/`

### Comprimir un archivo de texto

1. Ejecuta `python main.py`
2. Selecciona "Comprimir/Descomprimir Texto"
3. Haz clic en "Seleccionar archivo .txt"
4. Navega a `archivos/originales/` y selecciona tu archivo
5. Haz clic en "Comprimir"
6. El archivo comprimido se guardará en `archivos/comprimidos/` con extensión `.bin`

### Descomprimir un archivo

1. En la ventana correspondiente, haz clic en "Seleccionar y Descomprimir archivo .bin"
2. Navega a `archivos/comprimidos/` y selecciona el archivo comprimido
3. El archivo descomprimido se guardará automáticamente en `archivos/descomprimidos/`

### Reproducir y detener audio

1. Después de descomprimir un archivo de audio, haz clic en "Reproducir último archivo descomprimido"
2. Para detener la reproducción en cualquier momento, haz clic en el botón rojo "Detener Reproducción"
3. No es necesario cerrar la aplicación para detener el audio

## Estadísticas de Compresión

La aplicación muestra estadísticas detalladas para cada tipo de compresión:

### Para Texto (Huffman):

- Tamaño original del archivo .txt
- Tamaño del archivo .bin comprimido (incluye diccionario Huffman)
- Ratio de compresión
- Porcentaje de reducción de tamaño

### Para Imágenes (RLE):

- Tamaño RAW de la imagen (ancho × alto × 3 canales RGB)
- Tamaño del archivo .bin comprimido
- Ratio de compresión comparado con datos RAW
- **Nota:** Se compara contra el tamaño RAW, no contra PNG/JPG (que ya están comprimidos)

### Para Audio (RLE + Huffman):

- Tamaño RAW del audio PCM (n_frames × sample_width × channels)
- Tamaño del archivo .hac comprimido (incluye metadata y árbol Huffman)
- Ratio de compresión comparado con datos RAW
- **Nota:** Se compara contra el tamaño RAW PCM, no contra el WAV (que incluye headers)

**Importante:** Para archivos pequeños o con alta aleatoriedad, el archivo comprimido puede ser más grande que el original debido al overhead de los metadatos (diccionarios, árboles, etc.). Esto es normal y esperado.

## Notas Importantes

### Compresión de Texto (Huffman)

- Los archivos de texto se comprimen mejor cuando tienen caracteres repetidos
- Archivos muy cortos pueden resultar más grandes debido al overhead del diccionario Huffman
- Para mejores resultados, usa archivos de texto de al menos 1-2 KB
- La compresión es más efectiva con texto que tiene alta frecuencia de caracteres específicos

### Compresión de Imágenes (RLE)

- Las imágenes con áreas de color uniforme se comprimen más eficientemente
- La comparación se hace contra el tamaño RAW (sin compresión), no contra PNG/JPG
- PNG y JPG ya están comprimidos, por eso RLE puede parecer "expandir" el archivo
- RLE funciona mejor con imágenes simples, dibujos, diagramas o capturas de pantalla

### Compresión de Audio (RLE + Huffman)

- El audio comprimido mantiene toda la calidad original (sin pérdida)
- La comparación se hace contra el tamaño RAW PCM, no contra el archivo WAV
- Audios muy complejos o con mucho ruido pueden no comprimir bien
- La combinación RLE + Huffman es especialmente efectiva para audio con patrones

### Overhead de Metadata

- Todos los algoritmos necesitan guardar información adicional (diccionarios, árboles, etc.)
- Esta metadata es necesaria para la descompresión
- Por eso archivos muy pequeños pueden no mostrar reducción de tamaño
- El overhead se vuelve insignificante con archivos más grandes

## Solución de Problemas

### Error: "PyAudio no está instalado"

- En Windows: `pip install pipwin && pipwin install pyaudio`
- En Linux: `sudo apt-get install python3-pyaudio`
- En macOS: `brew install portaudio && pip install pyaudio`

### Error: "No module named 'src'"

- Asegúrate de ejecutar `python main.py` desde la raíz del proyecto

### La compresión no reduce el tamaño (o lo aumenta)

- Esto es **completamente normal** para archivos muy pequeños o altamente aleatorios
- Los algoritmos de compresión requieren cierta redundancia para funcionar
- El overhead de metadata (diccionarios Huffman, árboles, etc.) puede ser mayor que el ahorro
- Usa archivos más grandes para ver la compresión real en acción
- Para imágenes: RLE se compara contra tamaño RAW, no contra PNG/JPG
- Para audio: RLE+Huffman se compara contra PCM RAW, no contra WAV

### Los archivos comprimidos son más grandes que los originales (PNG, JPG, WAV)

- **Esto es esperado:** PNG, JPG y WAV ya incluyen algún tipo de compresión/optimización
- Nuestros algoritmos comparan contra el tamaño RAW (sin comprimir) de los datos
- Por ejemplo: una imagen PNG de 50KB puede tener 500KB de datos RAW RGB
- Si RLE comprime a 300KB, **sí hay compresión** (500KB → 300KB), aunque sea más grande que el PNG original

## Licencia

Proyecto académico - Universidad Rafael Landívar
Estructura de Datos II - 2025

## Contacto

Para preguntas o problemas, contacta a los miembros del equipo.
