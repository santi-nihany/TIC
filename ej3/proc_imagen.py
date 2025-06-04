from PIL import Image
import numpy as np
from collections import Counter


def procesar_imagen(ruta: str, simbolos: list[str]) -> list[float]:
    """
    Procesa una imagen y devuelve las probabilidades de los patrones de los simbolos.

    Inputs:
        - ruta: Ruta de la imagen.
        - simbolos: Lista de simbolos (strings de bits, ej. "101", "000").

    Output:
        - probabilidades: Lista de probabilidades de los simbolos.
    """
    # Cargar la imagen y convertir a escala de grises
    imagen = Image.open(ruta).convert('L')

    # Convertir la imagen en un array numpy
    array = np.array(imagen)

    # Binarizar la imagen: negros = 1, blancos = 0
    umbral = 128
    binaria = (array < umbral).astype(int)

    # Aplanar en una secuencia de bits (puede recorrer por filas)
    bits = binaria.flatten()

    # Determinar el largo de los símbolos (asumimos que todos son del mismo tamaño)
    largo_patron = len(simbolos[0])

    # Crear lista de todos los patrones encontrados
    patrones_encontrados = []
    for i in range(len(bits) - largo_patron + 1):
        patron = ''.join(str(b) for b in bits[i:i + largo_patron])
        patrones_encontrados.append(patron)

    # Contar ocurrencias
    conteo = Counter(patrones_encontrados)

    total = sum(conteo[simbolo] for simbolo in simbolos)
    if total == 0:
        return [0.0 for _ in simbolos]

    # Calcular probabilidades
    probabilidades = [conteo[simbolo] / total for simbolo in simbolos]

    return probabilidades
