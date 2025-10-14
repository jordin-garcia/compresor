import numpy as np
import wave
import struct
import heapq
import os
import time
from collections import Counter
import pickle
import pyaudio
import threading
#etapa1
class NodoHuffman:
    __slots__ = ('simbolo', 'frecuencia', 'izquierda', 'derecha')
    
    def __init__(self, simbolo=None, frecuencia=None):
        self.simbolo = simbolo
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None
    
    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

class ReproductorAudio:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.reproduciendo = False
        self.hilo_reproduccion = None
        self.lock = threading.Lock()
    
    def reproducir_wav(self, ruta_archivo):
        """Reproduce un archivo WAV directamente"""
        try:
            if not os.path.exists(ruta_archivo):
                print(f"ERROR: Archivo no encontrado: {ruta_archivo}")
                return False
            
            self.detener_reproduccion()
            
            print(f"Reproduciendo: {os.path.basename(ruta_archivo)}")
            
            with wave.open(ruta_archivo, 'rb') as archivo:
                sample_width = archivo.getsampwidth()
                channels = archivo.getnchannels()
                frame_rate = archivo.getframerate()
                n_frames = archivo.getnframes()
                audio_data = archivo.readframes(n_frames)
            
            self.stream = self.audio.open(
                format=self.audio.get_format_from_width(sample_width),
                channels=channels,
                rate=frame_rate,
                output=True,
                frames_per_buffer=1024
            )
            
            self.reproduciendo = True
            self.hilo_reproduccion = threading.Thread(
                target=self._reproducir_datos, 
                args=(audio_data,),
                name="ReproductorAudio"
            )
            self.hilo_reproduccion.daemon = True
            self.hilo_reproduccion.start()
            
            duracion = n_frames / frame_rate
            print(f"   Duracion: {duracion:.1f} segundos")
            print(f"   Canales: {channels}, Sample Rate: {frame_rate}Hz")
            print("   Presiona 'Enter' y luego opcion 4 para detener...")
            
            return True
                
        except Exception as e:
            print(f"ERROR reproduciendo audio: {e}")
            return False
    
    def _reproducir_datos(self, audio_data):
        """Funcion interna para reproducir datos de audio desde memoria"""
        try:
            chunk_size = 1024
            total_bytes = len(audio_data)
            bytes_enviados = 0
            
            while bytes_enviados < total_bytes and self.reproduciendo:
                chunk = audio_data[bytes_enviados:bytes_enviados + chunk_size]
                if chunk:
                    self.stream.write(chunk)
                    bytes_enviados += len(chunk)
                else:
                    break
            
            if bytes_enviados >= total_bytes and self.reproduciendo:
                print("Reproduccion completada")
            
        except Exception as e:
            if self.reproduciendo:
                print(f"Error en reproduccion: {e}")
        
        finally:
            self._limpiar_recursos()
    
    def _limpiar_recursos(self):
        """Limpia los recursos de reproduccion de forma segura"""
        with self.lock:
            self.reproduciendo = False
            if self.stream:
                try:
                    self.stream.stop_stream()
                    self.stream.close()
                    self.stream = None
                except Exception as e:
                    print(f"Error limpiando stream: {e}")
    
    def detener_reproduccion(self):
        """Detiene la reproduccion actual de forma segura"""
        with self.lock:
            if not self.reproduciendo:
                return
            
            self.reproduciendo = False
            
            if self.stream:
                try:
                    self.stream.stop_stream()
                    self.stream.close()
                    self.stream = None
                except Exception as e:
                    print(f"Error deteniendo stream: {e}")
            
            if (self.hilo_reproduccion and 
                self.hilo_reproduccion.is_alive() and 
                self.hilo_reproduccion != threading.current_thread()):
                
                self.hilo_reproduccion.join(timeout=2.0)
                if self.hilo_reproduccion.is_alive():
                    print("AVISO: El hilo de reproduccion no termino correctamente")
            
            self.hilo_reproduccion = None
            print("Reproduccion detenida")
    
    def esta_reproduciendo(self):
        """Verifica si esta reproduciendo"""
        return self.reproduciendo
    
    def __del__(self):
        """Limpiar recursos"""
        self.detener_reproduccion()
        if self.audio:
            try:
                self.audio.terminate()
            except:
                pass

class CompresorAudioOptimizado:
    def __init__(self):
        self.codigos_huffman = {}
        self.arbol_huffman = None
        self.reproductor = ReproductorAudio()
    
    def construir_arbol_huffman(self, datos):
        """Construye arbol de Huffman optimizado"""
        print("  Contando frecuencias...")
        
        valores_unicos, conteos = np.unique(datos, return_counts=True)
        frecuencias = dict(zip(valores_unicos, conteos))
        
        print(f"  Simbolos unicos: {len(frecuencias)}")
        
        cola_prioridad = [NodoHuffman(simbolo, freq) for simbolo, freq in frecuencias.items()]
        heapq.heapify(cola_prioridad)
        
        while len(cola_prioridad) > 1:
            nodo1 = heapq.heappop(cola_prioridad)
            nodo2 = heapq.heappop(cola_prioridad)
            
            nodo_combinado = NodoHuffman(frecuencia=nodo1.frecuencia + nodo2.frecuencia)
            nodo_combinado.izquierda = nodo1
            nodo_combinado.derecha = nodo2
            
            heapq.heappush(cola_prioridad, nodo_combinado)
        
        return cola_prioridad[0]
    
    def comprimir_rle(self, datos):
        """RLE vectorizado usando numpy"""
        print("  Aplicando RLE vectorizado...")
        
        if len(datos) == 0:
            return np.array([], dtype=np.int32)
        
        cambios = np.where(datos[1:] != datos[:-1])[0] + 1
        cambios = np.concatenate(([0], cambios, [len(datos)]))
        
        longitudes = cambios[1:] - cambios[:-1]
        valores = datos[cambios[:-1]]
        
        comprimido = np.empty(len(valores) + len(longitudes), dtype=np.int32)
        comprimido[0::2] = valores
        comprimido[1::2] = longitudes
        
        print(f"  RLE completado: {len(comprimido)} elementos")
        return comprimido
    
    def descomprimir_rle(self, datos_comprimidos):
        """RLE inverso vectorizado"""
        print("  Descomprimiendo RLE vectorizado...")
        
        if len(datos_comprimidos) == 0:
            return np.array([], dtype=np.int32)
        
        valores = datos_comprimidos[0::2]
        longitudes = datos_comprimidos[1::2]
        
        descomprimido = np.repeat(valores, longitudes)
        
        print(f"  RLE descomprimido: {len(descomprimido)} muestras")
        return descomprimido
    
    def codificar_huffman(self, datos_rle, codigos_huffman):
        """Codificacion Huffman optimizada"""
        print("  Codificando Huffman...")
        
        longitudes = {simbolo: len(codigo) for simbolo, codigo in codigos_huffman.items()}
        bits_totales = sum(longitudes[valor] for valor in datos_rle)
        bytes_totales = (bits_totales + 7) // 8
        
        resultado = bytearray(bytes_totales)
        bit_actual = 0
        
        for valor in datos_rle:
            codigo = codigos_huffman[valor]
            for bit in codigo:
                if bit == '1':
                    resultado[bit_actual // 8] |= (1 << (7 - (bit_actual % 8)))
                bit_actual += 1
        
        print(f"  Huffman codificado: {len(resultado)} bytes")
        return bytes(resultado), bit_actual
    
    def decodificar_huffman(self, bits_comprimidos, bits_validos, arbol_raiz):
        """Decodificacion Huffman optimizada"""
        print("  Decodificando Huffman...")
        
        datos_rle = []
        nodo_actual = arbol_raiz
        
        bits_array = []
        for byte in bits_comprimidos:
            for i in range(7, -1, -1):
                bits_array.append((byte >> i) & 1)
        
        bits_array = bits_array[:bits_validos]
        
        for bit in bits_array:
            if bit == 0:
                nodo_actual = nodo_actual.izquierda
            else:
                nodo_actual = nodo_actual.derecha
            
            if nodo_actual.simbolo is not None:
                datos_rle.append(nodo_actual.simbolo)
                nodo_actual = arbol_raiz
        
        print(f"  Huffman decodificado: {len(datos_rle)} elementos")
        return np.array(datos_rle, dtype=np.int32)
    
    def comprimir_audio(self, ruta_archivo):
        """Compresion optimizada y rapida"""
        print("\n=== COMPRESION INICIADA ===")
        inicio = time.time()
        
        try:
            with wave.open(ruta_archivo, 'rb') as archivo_wav:
                canales = archivo_wav.getnchannels()
                sample_width = archivo_wav.getsampwidth()
                frame_rate = archivo_wav.getframerate()
                n_frames = archivo_wav.getnframes()
                frames = archivo_wav.readframes(n_frames)
                
                if sample_width == 1:
                    datos_audio = np.frombuffer(frames, dtype=np.uint8)
                elif sample_width == 2:
                    datos_audio = np.frombuffer(frames, dtype=np.int16)
                else:
                    datos_audio = np.frombuffer(frames, dtype=np.uint8)
            
            print(f"  Muestras a procesar: {len(datos_audio):,}")
            
            tiempo_rle = time.time()
            datos_rle = self.comprimir_rle(datos_audio)
            tiempo_rle = time.time() - tiempo_rle
            
            tiempo_huffman = time.time()
            self.arbol_huffman = self.construir_arbol_huffman(datos_rle)
            self.codigos_huffman = {}
            self._generar_codigos_huffman(self.arbol_huffman)
            tiempo_huffman = time.time() - tiempo_huffman
            
            tiempo_codificacion = time.time()
            bits_comprimidos, bits_validos = self.codificar_huffman(datos_rle, self.codigos_huffman)
            tiempo_codificacion = time.time() - tiempo_codificacion
            
            nombre_base = os.path.splitext(ruta_archivo)[0]
            ruta_comprimido = nombre_base + "_comprimido.hac"
            
            with open(ruta_comprimido, 'wb') as f:
                metadatos = {
                    'canales': canales,
                    'sample_width': sample_width,
                    'frame_rate': frame_rate,
                    'tamano_original': len(datos_audio),
                    'bits_validos': bits_validos,
                    'arbol_huffman': self._serializar_arbol(self.arbol_huffman)
                }
                pickle.dump(metadatos, f)
                f.write(bits_comprimidos)
            
            tiempo_total = time.time() - inicio
            tamano_original = len(datos_audio) * sample_width
            ratio_compresion = tamano_original / len(bits_comprimidos) if len(bits_comprimidos) > 0 else 1
            
            print(f"\n=== COMPRESION COMPLETADA ===")
            print(f"Tiempo total: {tiempo_total:.2f}s")
            print(f" - RLE: {tiempo_rle:.2f}s")
            print(f" - Huffman: {tiempo_huffman:.2f}s") 
            print(f" - Codificacion: {tiempo_codificacion:.2f}s")
            print(f"Ratio compresion: {ratio_compresion:.2f}:1")
            print(f"Archivo: {ruta_comprimido}")
            
            return True
            
        except Exception as e:
            print(f"ERROR en compresion: {e}")
            return False
    
    def descomprimir_audio(self, ruta_comprimido):
        """Descompresion optimizada y rapida"""
        print("\n=== DESCOMPRESION INICIADA ===")
        inicio = time.time()
        
        try:
            with open(ruta_comprimido, 'rb') as f:
                metadatos = pickle.load(f)
                bits_comprimidos = f.read()
            
            self.arbol_huffman = self._reconstruir_arbol(metadatos['arbol_huffman'])
            
            tiempo_decodificacion = time.time()
            datos_rle = self.decodificar_huffman(
                bits_comprimidos, 
                metadatos['bits_validos'], 
                self.arbol_huffman
            )
            tiempo_decodificacion = time.time() - tiempo_decodificacion
            
            tiempo_rle = time.time()
            datos_audio = self.descomprimir_rle(datos_rle)
            tiempo_rle = time.time() - tiempo_rle
            
            nombre_base = os.path.splitext(ruta_comprimido)[0]
            ruta_descomprimido = nombre_base + "_descomprimido.wav"
            
            with wave.open(ruta_descomprimido, 'wb') as archivo_wav:
                archivo_wav.setnchannels(metadatos['canales'])
                archivo_wav.setsampwidth(metadatos['sample_width'])
                archivo_wav.setframerate(metadatos['frame_rate'])
                
                if metadatos['sample_width'] == 1:
                    frames_data = datos_audio.astype(np.uint8).tobytes()
                else:
                    frames_data = datos_audio.astype(np.int16).tobytes()
                
                archivo_wav.writeframes(frames_data)
            
            tiempo_total = time.time() - inicio
            
            print(f"\n=== DESCOMPRESION COMPLETADA ===")
            print(f"Tiempo total: {tiempo_total:.2f}s")
            print(f" - Decodificacion: {tiempo_decodificacion:.2f}s")
            print(f" - RLE: {tiempo_rle:.2f}s")
            print(f"Muestras reconstruidas: {len(datos_audio):,}")
            print(f"Archivo: {ruta_descomprimido}")
            
            return ruta_descomprimido
            
        except Exception as e:
            print(f"ERROR en descompresion: {e}")
            return None
    
    def reproducir_audio(self, ruta_archivo):
        """Reproduce un archivo de audio (WAV o descomprimido)"""
        if not os.path.exists(ruta_archivo):
            print(f"ERROR: Archivo no encontrado: {ruta_archivo}")
            return False
        
        if self.reproductor.esta_reproduciendo():
            print("AVISO: Ya hay una reproduccion en curso. Deteniendo...")
            self.detener_reproduccion()
            time.sleep(0.5)
        
        if ruta_archivo.endswith('.hac'):
            print("AVISO: Los archivos .hac estan comprimidos. Descomprimiendo primero...")
            ruta_descomprimido = self.descomprimir_audio(ruta_archivo)
            if ruta_descomprimido:
                print("Reproduciendo archivo descomprimido...")
                return self.reproductor.reproducir_wav(ruta_descomprimido)
            else:
                return False
        else:
            return self.reproductor.reproducir_wav(ruta_archivo)
    
    def detener_reproduccion(self):
        """Detiene la reproduccion actual"""
        self.reproductor.detener_reproduccion()
    
    def esta_reproduciendo(self):
        """Verifica si esta reproduciendo"""
        return self.reproductor.esta_reproduciendo()
    
    def _generar_codigos_huffman(self, nodo, codigo_actual=""):
        if nodo is None:
            return
        if nodo.simbolo is not None:
            self.codigos_huffman[nodo.simbolo] = codigo_actual
            return
        self._generar_codigos_huffman(nodo.izquierda, codigo_actual + "0")
        self._generar_codigos_huffman(nodo.derecha, codigo_actual + "1")
    
    def _serializar_arbol(self, nodo):
        if nodo is None:
            return None
        if nodo.simbolo is not None:
            return {'simbolo': nodo.simbolo, 'frecuencia': nodo.frecuencia, 'hoja': True}
        return {
            'frecuencia': nodo.frecuencia,
            'hoja': False,
            'izquierda': self._serializar_arbol(nodo.izquierda),
            'derecha': self._serializar_arbol(nodo.derecha)
        }
    
    def _reconstruir_arbol(self, arbol_serializado):
        if arbol_serializado is None:
            return None
        if arbol_serializado.get('hoja', False):
            return NodoHuffman(arbol_serializado['simbolo'], arbol_serializado['frecuencia'])
        nodo = NodoHuffman(frecuencia=arbol_serializado['frecuencia'])
        nodo.izquierda = self._reconstruir_arbol(arbol_serializado['izquierda'])
        nodo.derecha = self._reconstruir_arbol(arbol_serializado['derecha'])
        return nodo

def crear_archivo_prueba():
    """Crea archivo de prueba optimizado"""
    print("Creando archivo de prueba...")
    
    sample_rate = 44100
    duration = 2
    t = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    
    señal = (np.sin(2 * np.pi * 440 * t) * 0.6 + 
             np.sin(2 * np.pi * 880 * t) * 0.4) * 32767
    audio_data = señal.astype(np.int16)
    
    with wave.open("audio_prueba.wav", 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(audio_data.tobytes())
    
    print("Archivo de prueba creado: audio_prueba.wav")
    return "audio_prueba.wav"

def main():
    compresor = CompresorAudioOptimizado()
    
    archivo_prueba = "audio_prueba.wav"
    if not os.path.exists(archivo_prueba):
        archivo_prueba = crear_archivo_prueba()
    
    while True:
        print("\n" + "="*50)
        print("COMPRESOR + REPRODUCTOR DE AUDIO")
        print("="*50)
        print("1. Comprimir archivo WAV")
        print("2. Descomprimir archivo .hac") 
        print("3. Reproducir archivo de audio")
        print("4. Detener reproduccion")
        print("5. Probar flujo completo")
        print("6. Salir")
        print("-"*50)
        
        if compresor.esta_reproduciendo():
            print("Reproduccion en curso...")
        
        opcion = input("Selecciona una opcion: ").strip()
        
        if opcion == "1":
            archivo = input("Ruta del archivo WAV a comprimir: ").strip()
            if os.path.exists(archivo):
                compresor.comprimir_audio(archivo)
            else:
                print("ERROR: El archivo no existe")
        
        elif opcion == "2":
            archivo = input("Ruta del archivo .hac a descomprimir: ").strip()
            if os.path.exists(archivo):
                resultado = compresor.descomprimir_audio(archivo)
                if resultado:
                    print(f"¿Quieres reproducir el archivo descomprimido? (s/n): ")
                    if input().strip().lower() == 's':
                        compresor.reproducir_audio(resultado)
            else:
                print("ERROR: El archivo no existe")
        
        elif opcion == "3":
            archivo = input("Ruta del archivo a reproducir (WAV o .hac): ").strip()
            compresor.reproducir_audio(archivo)
        
        elif opcion == "4":
            compresor.detener_reproduccion()
        
        elif opcion == "5":
            print("Probando flujo completo...")
            print("1. Comprimiendo archivo de prueba...")
            if compresor.comprimir_audio(archivo_prueba):
                print("2. Descomprimiendo archivo...")
                resultado = compresor.descomprimir_audio("audio_prueba_comprimido.hac")
                if resultado:
                    print("3. Reproduciendo archivo descomprimido...")
                    compresor.reproducir_audio(resultado)
                    print("La reproduccion comenzo. Puedes:")
                    print("   - Esperar a que termine naturalmente")
                    print("   - Usar la opcion 4 para detenerla")
        
        elif opcion == "6":
            compresor.detener_reproduccion()
            print("Hasta luego!")
            break
        
        else:
            print("Opcion no valida")

if __name__ == "__main__":
    try:
        import pyaudio
        print("PyAudio esta instalado correctamente")
    except ImportError:
        print("ERROR: PyAudio no esta instalado.")
        print("Para instalar: pip install pyaudio")
        print("En Windows: pip install pipwin && pipwin install pyaudio")
        exit(1)
    
    main()