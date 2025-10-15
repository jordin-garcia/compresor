import heapq
import pickle
from collections import defaultdict


class Nodo:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.izq = None
        self.der = None

    def __lt__(self, otro):
        return self.freq < otro.freq


def construir_arbol(freqs):
    heap = [Nodo(c, f) for c, f in freqs.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        izq = heapq.heappop(heap)
        der = heapq.heappop(heap)
        nodo = Nodo(None, izq.freq + der.freq)
        nodo.izq, nodo.der = izq, der
        heapq.heappush(heap, nodo)

    return heap[0]


def generar_codigos(nodo, prefijo="", codigos=None):
    if codigos is None:
        codigos = {}
    if nodo is None:
        return codigos
    if nodo.char is not None:  # hoja
        codigos[nodo.char] = prefijo
    generar_codigos(nodo.izq, prefijo + "0", codigos)
    generar_codigos(nodo.der, prefijo + "1", codigos)
    return codigos


def comprimir_texto(texto, archivo_salida="comprimido.bin"):
    # 1. Frecuencias
    freqs = defaultdict(int)
    for c in texto:
        freqs[c] += 1

    # 2. Árbol y códigos
    raiz = construir_arbol(freqs)
    codigos = generar_codigos(raiz)

    # 3. Codificar el texto
    bits = "".join(codigos[c] for c in texto)

    # 4. Padding a múltiplo de 8
    extra_padding = 8 - len(bits) % 8
    bits += "0" * extra_padding
    padded_info = "{0:08b}".format(extra_padding)
    bits = padded_info + bits

    # 5. Convertir a bytes
    b = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i : i + 8]
        b.append(int(byte, 2))

    # 6. Guardar en binario (pickle guarda codigos + data)
    with open(archivo_salida, "wb") as f:
        pickle.dump((codigos, b), f)

    print(f"Texto comprimido y guardado en {archivo_salida}")
    return codigos


def descomprimir_texto(archivo_entrada="comprimido.bin", archivo_salida="salida.txt"):
    with open(archivo_entrada, "rb") as f:
        codigos, b = pickle.load(f)

    # Invertir diccionario
    reverse = {v: k for k, v in codigos.items()}

    # Bytes → string de bits
    bit_string = ""
    for byte in b:
        bit_string += f"{byte:08b}"

    # Quitar padding
    extra_padding = int(bit_string[:8], 2)
    bit_string = bit_string[8:]
    bit_string = bit_string[:-extra_padding]

    # Decodificar
    current = ""
    texto = ""
    for bit in bit_string:
        current += bit
        if current in reverse:
            texto += reverse[current]
            current = ""

    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write(texto)

    print(f"Texto descomprimido y guardado en {archivo_salida}")
    return texto
