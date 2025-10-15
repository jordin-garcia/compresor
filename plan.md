# Plan de Desarrollo - Proyecto 3: Compresor de Datos

## Información del Equipo

- **Elizabeth**: Compresión de Audio
- **Cristian**: Compresión de Imágenes
- **André**: Compresión de Texto
- **Jordin**: Interfaz Gráfica
- **Fecha de entrega**: 16 de octubre, 23:59

---

## Estructura del Proyecto

```
compresor/
│
├── main.py                      # Punto de entrada principal
├── README.md                    # Documentación del proyecto
├── requirements.txt             # Dependencias del proyecto
│
├── src/
│   ├── compresion_texto.py     # Módulo de André
│   ├── compresion_imagen.py    # Módulo de Cristian
│   └── compresion_audio.py    # Módulo de Elizabeth
│   └── interfaz_grafica.py    # Módulo de Jordin
│
├── archivos/   
│   ├── comprimidos/		# Carpeta para archivos comprimidos
│   ├── pruebas/		# Archivos de prueba  
```

---

## Fase 1: Configuración Inicial (Día 1)

### Todos los miembros del equipo

1. **Crear repositorio en GitHub**

   - Crear repo público o privado
   - Invitar a todos los colaboradores
   - Configurar `.gitignore` para Python:
     ```
     __pycache__/
     *.pyc
     *.pyo
     .venv/
     venv/
     output/
     *.bin
     *.rle
     ```
2. **Clonar repositorio localmente**

   ```bash
   git clone [URL_DEL_REPO]
   cd proyecto-compresor
   ```
3. **Crear estructura de carpetas**

   ```bash
   mkdir gui compression utils tests output
   touch main.py requirements.txt README.md
   touch gui/__init__.py gui/interface.py
   touch compression/__init__.py compression/text_compression.py
   touch compression/image_compression.py compression/audio_compression.py
   touch utils/__init__.py utils/file_handler.py
   ```
4. **Crear `requirements.txt` inicial**

   ```
   tkinter
   pillow
   numpy
   pydub
   ```
5. **Crear ramas de trabajo**

   ```bash
   git checkout -b feature/text-compression    # André
   git checkout -b feature/image-compression   # Cristian
   git checkout -b feature/audio-compression   # Elizabeth
   git checkout -b feature/gui                 # Tú
   ```

---

## Fase 2: Desarrollo de Módulos Individuales (Días 2-5)

### André - Compresión de Texto (Huffman)

**Archivo: `src/compresion_texto.py`**

#### Funciones a implementar:

```python
def compress_text(input_file_path, output_file_path):
    """
    Comprime un archivo de texto usando Huffman
    Args:
        input_file_path: ruta del archivo .txt
        output_file_path: ruta donde guardar .bin
    Returns:
        dict con información: tamaño_original, tamaño_comprimido, ratio
    """
    pass

def decompress_text(compressed_file_path, output_file_path):
    """
    Descomprime un archivo .bin a .txt
    Args:
        compressed_file_path: ruta del archivo .bin
        output_file_path: ruta donde guardar .txt
    Returns:
        bool indicando éxito
    """
    pass
```

#### Pasos de implementación:

1. **Crear tabla de frecuencias**

   - Leer el archivo
   - Contar frecuencia de cada carácter
2. **Construir árbol de Huffman**

   - Usar una cola de prioridad (heapq)
   - Crear nodos hoja para cada carácter
   - Combinar nodos hasta tener un árbol
3. **Generar códigos**

   - Recorrer el árbol
   - Asignar códigos binarios (0=izquierda, 1=derecha)
4. **Comprimir**

   - Convertir texto a string de bits usando códigos
   - Guardar el árbol/diccionario y los bits en archivo .bin
5. **Descomprimir**

   - Leer el árbol/diccionario del archivo
   - Reconstruir texto usando los bits

#### Estructura del archivo .bin:

```
[longitud_diccionario][diccionario_serializado][bits_comprimidos]
```

---

### Cristian - Compresión de Imágenes (RLE)

**Archivo: `src/compresion_imagen.py`**

#### Funciones a implementar:

```python
def compress_image(input_file_path, output_file_path):
    """
    Comprime imagen usando RLE píxel por píxel
    Args:
        input_file_path: ruta de imagen .png o .bmp
        output_file_path: ruta donde guardar .rle
    Returns:
        dict con información: tamaño_original, tamaño_comprimido, ratio
    """
    pass

def decompress_image(compressed_file_path, output_file_path):
    """
    Descomprime y reconstruye imagen
    Args:
        compressed_file_path: ruta del archivo .rle
        output_file_path: ruta donde guardar imagen
    Returns:
        bool indicando éxito
    """
    pass
```

#### Pasos de implementación:

1. **Cargar imagen**

   ```python
   from PIL import Image
   img = Image.open(input_file_path)
   pixels = list(img.getdata())
   width, height = img.size
   mode = img.mode  # RGB, RGBA, L, etc.
   ```
2. **Aplicar RLE**

   - Recorrer lista de píxeles
   - Contar píxeles consecutivos iguales
   - Formato: `[count, pixel_value, count, pixel_value, ...]`
3. **Guardar archivo .rle**

   - Guardar metadatos: ancho, alto, modo
   - Guardar datos comprimidos
4. **Descomprimir**

   - Leer metadatos
   - Expandir RLE a lista de píxeles
   - Reconstruir imagen con PIL

#### Estructura del archivo .rle:

```
[width][height][mode][rle_data]
```

---

### Elizabeth - Compresión de Audio (RLE/Huffman en WAV)

**Archivo: `src/compresion_audio.py`**

#### Funciones a implementar:

```python
def compress_audio(input_file_path, output_file_path):
    """
    Comprime audio WAV usando RLE o Huffman
    Args:
        input_file_path: ruta del archivo .wav
        output_file_path: ruta donde guardar comprimido
    Returns:
        dict con información: tamaño_original, tamaño_comprimido, ratio
    """
    pass

def decompress_audio(compressed_file_path, output_file_path):
    """
    Descomprime y reconstruye audio WAV
    Args:
        compressed_file_path: ruta del archivo comprimido
        output_file_path: ruta donde guardar .wav
    Returns:
        bool indicando éxito
    """
    pass
```

#### Pasos de implementación:

1. **Cargar audio WAV**

   ```python
   import wave
   with wave.open(input_file_path, 'rb') as wav:
       params = wav.getparams()
       frames = wav.readframes(params.nframes)
   ```
2. **Aplicar compresión simple**

   - Opción 1: RLE en los bytes del audio
   - Opción 2: Huffman en los bytes del audio
   - Recomendación: usar RLE por simplicidad
3. **Guardar archivo comprimido**

   - Guardar parámetros del WAV (rate, channels, etc.)
   - Guardar datos comprimidos
4. **Descomprimir**

   - Leer parámetros
   - Expandir datos
   - Reconstruir archivo WAV

#### Estructura del archivo comprimido:

```
[params_serializados][datos_comprimidos]
```

---

### Jordin - Interfaz Gráfica

**Archivo: `src/interfaz_grafica.py`**

#### Estructura principal:

```python
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from compression import text_compression, image_compression, audio_compression

class CompressionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Compresor de Datos - Proyecto 3")
        self.root.geometry("600x400")
        self.create_main_menu()
  
    def create_main_menu(self):
        """Crea menú principal con 3 botones"""
        pass
  
    def open_text_window(self):
        """Abre ventana de compresión de texto"""
        pass
  
    def open_image_window(self):
        """Abre ventana de compresión de imágenes"""
        pass
  
    def open_audio_window(self):
        """Abre ventana de compresión de audio"""
        pass
```

#### Pasos de implementación:

1. **Menú Principal**

   - Título de la aplicación
   - 3 botones grandes y centrados
   - Diseño limpio y simple
2. **Ventana de Compresión de Texto**

   - Botón "Seleccionar archivo .txt"
   - Botón "Comprimir"
   - Label mostrando tamaño original vs comprimido
   - Botón "Descomprimir"
   - Botón "Volver al menú"
3. **Ventana de Compresión de Imágenes**

   - Similar a texto pero para .png/.bmp
   - Mostrar preview de imagen (opcional)
4. **Ventana de Compresión de Audio**

   - Similar a texto pero para .wav
   - Botón "Reproducir original" (opcional)
5. **Manejo de errores**

   - Try-except en todas las operaciones
   - Mostrar mensajes con `messagebox.showerror()`
   - Validar formatos de archivo

#### Ejemplo de ventana de compresión:

```python
def open_text_window(self):
    window = tk.Toplevel(self.root)
    window.title("Compresión de Texto")
    window.geometry("500x400")
  
    # Variables
    self.text_file_path = tk.StringVar()
  
    # Widgets
    tk.Label(window, text="Compresión de Texto (Huffman)", 
             font=("Arial", 14, "bold")).pack(pady=20)
  
    # Botón seleccionar archivo
    tk.Button(window, text="Seleccionar archivo .txt",
              command=self.select_text_file).pack(pady=10)
  
    # Label mostrar archivo seleccionado
    tk.Label(window, textvariable=self.text_file_path).pack()
  
    # Botón comprimir
    tk.Button(window, text="Comprimir", 
              command=self.compress_text_action).pack(pady=10)
  
    # Frame para resultados
    self.text_result_frame = tk.Frame(window)
    self.text_result_frame.pack(pady=10)
  
    # Botón descomprimir
    tk.Button(window, text="Descomprimir",
              command=self.decompress_text_action).pack(pady=10)
  
    # Botón volver
    tk.Button(window, text="Volver al menú",
              command=window.destroy).pack(pady=20)
```

---

## Fase 3: Integración (Días 6-7)

### Archivo Principal: `main.py`

```python
import tkinter as tk
from gui.interface import CompressionApp

def main():
    root = tk.Tk()
    app = CompressionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

### Pasos de integración:

1. **Cada uno hace merge de su rama a `main`**

   ```bash
   git checkout main
   git pull origin main
   git merge feature/[nombre-feature]
   git push origin main
   ```
2. **Resolver conflictos si los hay**
3. **Probar integración completa**

   - Cada módulo debe funcionar independientemente
   - La GUI debe llamar correctamente a cada módulo
   - Verificar manejo de errores
4. **Crear archivos de prueba en `tests/`**

   - sample.txt con texto variado
   - sample.png con pocos colores
   - sample.wav archivo corto

---

## Fase 4: Pruebas y Refinamiento (Día 8)

### Lista de verificación:

- [ ] **Texto**: Comprime y descomprime correctamente
- [ ] **Imágenes**: Comprime y reconstruye imagen idéntica
- [ ] **Audio**: Comprime y reproduce correctamente
- [ ] **Interfaz**: Todos los botones funcionan
- [ ] **Comparación**: Muestra tamaños original vs comprimido
- [ ] **Errores**: Maneja archivos incorrectos sin crashear
- [ ] **Alertas**: Muestra mensajes al usuario
- [ ] **Archivos**: Guarda en rutas correctas

### Pruebas específicas:

1. **Texto**

   - Archivo vacío
   - Texto muy corto
   - Texto con caracteres especiales
   - Texto largo (>1MB)
2. **Imágenes**

   - Imagen monocromática
   - Imagen con pocos colores
   - Imagen compleja (verificar que funcione aunque no comprima bien)
3. **Audio**

   - Audio corto
   - Audio largo
   - Diferentes frecuencias de muestreo

---

## Fase 5: Documentación Final (Día 9)

### Actualizar `README.md`:

```markdown
# Proyecto 3: Compresor de Datos

## Integrantes
- Elizabeth - Compresión de Audio
- Cristian - Compresión de Imágenes
- André - Compresión de Texto
- Jordin - Interfaz Gráfica

## Descripción
Aplicación de compresión de datos que implementa:
- Compresión de texto con algoritmo Huffman
- Compresión de imágenes con RLE
- Compresión de audio con RLE

## Requisitos
- Python 3.8+
- Ver requirements.txt

## Instalación
```bash
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

## Estructura del Proyecto

[Copiar estructura de carpetas]

```

---

## Consejos para Trabajo en Equipo

### Comunicación:

1. **Crear grupo de WhatsApp/Discord**
2. **Reuniones breves diarias** (5-10 min)
   - ¿Qué hice ayer?
   - ¿Qué haré hoy?
   - ¿Tengo algún bloqueador?

3. **Usar Issues en GitHub** para reportar problemas

### Buenas prácticas Git:

1. **Commits descriptivos**
```

   ✅ "Implementa compresión Huffman para texto"
   ❌ "fix"

```

2. **Push frecuente** (al menos una vez al día)

3. **Pull antes de trabajar**
   ```bash
   git pull origin main
```

4. **No subir archivos grandes** al repo
5. **Usar .gitignore** correctamente

### División de tareas clara:

- **André**: Solo trabaja en  `src/compresion_texto.py`
- **Cristian**: Solo trabaja en `src/compresion_imagen.py`
- **Elizabeth**: Solo trabaja en `src/compresion_audio.py`
- **Jordin:** Solo trabaja en `src/interfaz_grafica.py`

Esto evita conflictos de merge.

---

## Checklist de Entrega

### Antes del 16 de octubre:

- [ ] Código subido a GitHub
- [ ] Todos los módulos funcionan
- [ ] Interfaz completa y funcional
- [ ] README.md completo
- [ ] requirements.txt actualizado
- [ ] Archivos de prueba incluidos
- [ ] Código comentado y limpio
- [ ] Manejo de errores implementado
- [ ] Probado en al menos 2 computadoras diferentes

### Demostración en clase:

- [ ] Preparar archivos de ejemplo
- [ ] Ensayar demostración (5 minutos)
- [ ] Cada persona explica su parte
- [ ] Mostrar comparación de tamaños
- [ ] Demostrar manejo de errores

---

## Recursos Útiles

### Algoritmo Huffman:

- [Tutorial Python](https://www.geeksforgeeks.org/huffman-coding-greedy-algo-3/)

### Run Length Encoding:

- [Explicación RLE](https://en.wikipedia.org/wiki/Run-length_encoding)

### Tkinter:

- [Documentación oficial](https://docs.python.org/3/library/tkinter.html)
- [Tutorial Real Python](https://realpython.com/python-gui-tkinter/)

### PIL/Pillow:

- [Documentación Pillow](https://pillow.readthedocs.io/)

---

## Cronograma Sugerido

| Día | Actividad                           | Responsables           |
| ---- | ----------------------------------- | ---------------------- |
| 1    | Configuración inicial y estructura | Todos                  |
| 2-3  | Desarrollo individual               | Cada uno en su módulo |
| 4    | Primera prueba de integración      | Todos                  |
| 5    | Completar funcionalidades faltantes | Cada uno en su módulo |
| 6    | Integración final                  | Todos                  |
| 7    | Pruebas exhaustivas                 | Todos                  |
| 8    | Corrección de bugs                 | Todos                  |
| 9    | Documentación y preparación demo  | Todos                  |

---

## Contacto y Dudas

- **Repositorio**: [Agregar URL]
- **Líder de proyecto**: [Definir quién coordina]

---

## Notas Finales

1. **Simplicidad primero**: No complicar innecesariamente
2. **Funcionalidad sobre perfección**: Es mejor que funcione simple que no funcione complejo
3. **Comunicación constante**: Avisar si hay problemas temprano
4. **Ayuda mutua**: Si alguien termina antes, ayuda a los demás
5. **Prueben frecuentemente**: No esperen al final para probar

**¡Éxito en el proyecto!** 🚀
