import numpy as np


def detector(S: np.ndarray, R: np.ndarray, U: np.ndarray, k: int) -> tuple[int, int]:
    """
    Detecta y cuenta la cantidad de errores en las palabras de código recibidas.

    Args:
        S: Matriz de síndromes (m x n).
        R: Matriz de palabras de código recibidas (m x n).
        U: Matriz de palabras fuente originales (m x k).
        k: Longitud de las palabras fuente.

    Returns:
        tuple[int, int]: (cantidad de errores de bit, cantidad de errores de palabra)
    """
    # Obtener sindromes no nulos de S
    S_err = np.any(S != 0, axis=1)
    # Eliminar las palabras de R y U que correspondan a esos síndromes
    Ve = np.delete(R, S_err, axis=0)
    U = np.delete(U, S_err, axis=0)

    return get_errores(Ve, U, k)


def corrector(S: np.ndarray, R: np.ndarray, H: np.ndarray, U: np.ndarray, k: int) -> tuple[int, int]:
    """
    Corrige errores de un solo bit en palabras de código recibidas.

    Args:
        S: Matriz de síndromes (m x (n-k)).
        R: Matriz de palabras de código recibidas (m x n).
        H: Matriz de paridad (n x (n-k)).

    Returns:
        cant_errores: Número de palabras código con errores no corregidos.
    """
    m, n = R.shape

    for i in range(m):
        # Si el síndrome es distinto de 0
        if np.any(S[i]):
            # Comparar con filas de H
            for j in range(n):
                if np.array_equal(S[i], H[j]):
                    # Corregir el bit j de la palabra i
                    R[i, j] ^= 1
                    break  # Ya corregido
    # R = Ve
    return get_errores(R, U, k)


def get_errores(Ve: np.ndarray, U: np.ndarray, k: int) -> tuple[int, int]:
    # Codificación es sistemática -> decodificación: extraer la submatriz compuesta por las primeras k columnas de Ve
    Ue = Ve[:, :k]
    # Obtener una matriz de error E comparando la matriz de bits estimados Ue con los transmitidos U.
    E = np.logical_xor(U, Ue)

    # La cantidad de elementos no nulos de E será el número de bits errados
    cant_errores_bit = np.sum(E)
    # La cantidad de filas no nulas de E será el número de palabras erradas
    cant_errores_palabra = np.sum(np.any(E, axis=1))

    return cant_errores_bit, cant_errores_palabra
