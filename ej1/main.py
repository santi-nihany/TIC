import numpy as np
from cod import get_tc_dmin
from simulacion import simular_canal
from formulas import calcular_ga, to_db, Qinv
from resultados import plot_ganancia, crear_tabla, plot_prob_error


def main():
    # Seteo parametros del codigo
    n, k = 14, 10
    tc, dmin = get_tc_dmin(n, k)
    td = dmin - 1
    # Generar matriz de paridad P
    P = np.array([
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [1, 0, 0, 1],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 1, 0, 1],
        [1, 1, 1, 0],
        [0, 1, 1, 1],
        [1, 0, 1, 1]
    ])
    # Generar matriz generadora G y de paridad H transpuesta
    G = np.hstack((np.eye(k, dtype=int), P))
    H = np.hstack((P.T, np.eye(n-k, dtype=int))).T

    # Calcular la ganancia de codificación asintótica.
    Ga = to_db(calcular_ga(k, n, dmin))

    # Simulacion de canal AWGN
    # Eb/N0 = 1-7 [dB] | Paso: 0.25 db aprox
    EbN0_values = np.linspace(1, 7, 26)
    A = 1

    # 0 = Detector
    # 1 = Corrector
    DEC = 0

    (P_ep, P_eb) = simular_canal(G, H, EbN0_values, A, n, k, DEC)

    EbN0_sin_cod = to_db(Qinv(P_eb) ** 2 * 0.5)

    # Calcular ganancia de codigo
    Gc = EbN0_sin_cod - EbN0_values

    # Graficar resultados
    plot_prob_error(EbN0_values, P_eb, P_ep, DEC, n, tc, td)
    plot_ganancia(EbN0_values, Gc, Ga, DEC)

    # Crear tabla de resultados
    crear_tabla(EbN0_values, P_ep, P_eb, Gc, Ga, DEC)


if __name__ == "__main__":
    main()
