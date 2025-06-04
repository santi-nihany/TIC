import numpy as np
from awgn_bpsk import awgn_bpsk
from decod import detector, corrector
from formulas import Q, from_db, to_db


def simular_canal(G, H, EbN0_values, A, n, k, DEC):
    P_ep = np.zeros_like(EbN0_values, dtype=float)
    P_eb = np.zeros_like(EbN0_values, dtype=float)

    # Por cada fila de V (palabra a transmitir) -> retornar la palabra recibida al ingresar a awgn_bpsk y agrgarla a la matriz R
    for i, EbN0 in enumerate(EbN0_values):
        # Paso Eb/N0 de dB a veces
        EbfN0 = from_db(EbN0)

        P_ebt = Q(np.sqrt(2 * EbfN0))  # probabilidad de error de bit teorica

        # Calcular cant_palabras basado en la probabilidad de error teorica
        num_palabras = int((10**2) * (1/P_ebt))
        if (num_palabras < 10 ** 6):
            num_palabras = 10 ** 6

        # Generar U, matriz de dimensiones num_palabras x k con elementos 0 y 1 equiprobables e independientes.
        U = np.random.randint(0, 2, size=(num_palabras, k))

        # Obtener V = UG, matriz de dimensiones num_palabras x n cuyas filas serán las palabras de código transmitidas.
        V = np.dot(U, G) % 2

        # Simular canal AWGN
        R = awgn_bpsk(V, n, k, A, EbfN0)

        # Obtener síndromes
        S = np.dot(R, H) % 2

        # Decodificar
        if (DEC == 0):  # Detector
            cant_errores_bit, cant_errores_palabra = detector(S, R, U, k)
        else:  # Corrector
            cant_errores_bit, cant_errores_palabra = corrector(S, R, H, U, k)
        P_ep[i] = cant_errores_palabra / num_palabras
        P_eb[i] = cant_errores_bit / (k * num_palabras)

        print(f"Eb/N0: {EbN0:.2f} dB, P_eb: {P_eb[i]:.8f}")
        print(f"P_ebt: {P_ebt:.8f}")
    return P_ep, P_eb
