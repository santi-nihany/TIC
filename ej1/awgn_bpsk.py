import numpy as np


def awgn_bpsk(V: np.ndarray, n: int, k: int, A: float, EbfN0: float) -> np.ndarray:
    """
    Transmite una palabra de código v a través de un canal BPSK.

    Args:
        n (int): Largo de palabra de código.
        k (int): Largo de palabra de fuente.
        A (float): Amplitud de la señal BPSK.
        Es (float): Energía de símbolo de canal (Es = Eb para sistemas binarios).
        Ebf (float): Energía de bit de fuente.
        EbfN0 (float): Cociente energía de bit de fuente sobre densidad espectral de ruido deseado.
        V (np.ndarray): Matriz de palabras de código (m x n).

    Returns:
        vr (np.ndarray): Palabra de código recibida

    """
    Es = A**2
    Ebf = Es * n / k
    S = (2 * V - 1) * A
    N0 = Ebf / EbfN0
    noise = np.sqrt(
        N0 / 2) * (np.random.randn(V.shape[0], n) + 1j * np.random.randn(V.shape[0], n))
    R = S + noise
    Vr = (np.real(R) > 0).astype(int)
    return Vr
