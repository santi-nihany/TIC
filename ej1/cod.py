import numpy as np
from math import comb
from itertools import combinations


def get_tc_dmin(n: int, k: int) -> tuple[int, int]:
    """
    Calcula la cantidad de errores corregibles (tc) y la distancia mínima (dmin) usando la cota de Hamming.

    Args:
        n (int): Longitud total del código
        k (int): Longitud de la palabra de información

    Returns:
        tuple: (tc, dmin)
            - tc es la cantidad de errores corregibles
            - dmin es la distancia mínima de Hamming
            Si no se encuentra solución, retorna (-1, -1)
    """
    cota_hamming = 2 ** (n - k)
    MAX_ITER = 100
    res = 0
    # Obtener cantidad de errores (tc) corregibles usando cota de hamming
    for tc in range(0, MAX_ITER):
        res += comb(n, tc)  # combinaciones de n elementos tomados de a tc
        if (res > cota_hamming):  # si se supera la cota de hamming
            tc -= 1  # se resta 1 tc
            return (tc, (2 * tc) + 1)
    return (-1, -1)  # si no se encuentra, se retorna -1
