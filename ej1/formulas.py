import numpy as np
from scipy.special import erfc, erfcinv


def Q(x: float) -> float:
    return 0.5 * erfc(x / np.sqrt(2))


def Qinv(x: float) -> float:
    return np.sqrt(2) * erfcinv(2 * x)


def calcular_ga(k: int, n: int, dmin: int) -> float:
    """
    Calcula la ganancia de codificación asintótica Ga.

    Args:
        k: Número de bits de información.
        n: Longitud del código.
        dmin: Distancia de Hamming mínima.

    Returns:
        Ga: Ganancia de codificación asintótica.
    """
    Ga = (k / n) * np.floor((dmin + 1) / 2)
    return Ga


def to_db(x: float) -> float:
    """
    Convierte un valor a dB.

    Args:
        x: Valor a convertir.

    Returns:
        x_db: Valor en dB.
    """
    return 10 * np.log10(x)


def from_db(x: float) -> float:
    """
    Convierte un valor de dB a veces.

    Args:
        x: Valor a convertir.

    Returns:
        x_veces: Valor en veces.
    """
    return 10**(x/10)
