import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.special import comb
from formulas import Q, from_db
import os


def plot_prob_error(EbN0_db: np.ndarray, P_eb: np.ndarray, P_ep: np.ndarray, DEC: int, n: int, tc: int, td: int):
    # Convertir Eb/N0 de dB a veces
    EbN0_veces = from_db(EbN0_db)
    Peb_teorica_sc = Q(np.sqrt(2 * EbN0_veces))

    # Calcular curva teórica codificada
    if DEC == 0:  # Detector
        P_ebt_c = (comb(n, td + 1)) * (Peb_teorica_sc ** (td + 1))
    else:  # Corrector
        P_ebt_c = ((2 * tc + 1) / n) * comb(n, tc + 1) * \
            (Peb_teorica_sc ** (tc + 1))

    plt.figure(figsize=(10, 5))
    plt.semilogy(EbN0_db, P_eb, 'o-', label='Peb con codificación (simulado)')
    plt.semilogy(EbN0_db, P_ep, 's-', label='Pep con codificación (simulado)')
    plt.semilogy(EbN0_db, Peb_teorica_sc, 'k--',
                 label='Peb sin codificación (teórico)')
    plt.semilogy(EbN0_db, P_ebt_c, 'r--',
                 label='Peb con codificación (teórico)')
    plt.xlabel('$E_b/N_0$ [dB]')
    plt.ylabel('$P_e$')
    plt.title(f"Detector" if DEC == 0 else "Corrector")
    plt.grid(True, which='both', linestyle='-', alpha=0.5)
    plt.legend()
    plt.tight_layout()

    # Guardar el gráfico
    res_dir = os.path.join(os.path.dirname(__file__), 'resultados')
    os.makedirs(res_dir, exist_ok=True)
    if DEC == 0:
        nombre = "detector"
    else:
        nombre = "corrector"
    plt.savefig(os.path.join(res_dir, f'{nombre}_prob_error.png'))
    plt.show()


def plot_ganancia(EbN0_db: np.ndarray, Gc: np.ndarray, Ga: float, DEC: int):
    """
    Plotea la ganancia real (Gc) y la ganancia asintótica (Ga) en función de Eb/N0.

    Parámetros:
    - EbN0_db: Array de valores Eb/N0 [dB]
    - Gc: Array de ganancia real [dB]
    - Ga: Ganancia asintótica (constante) [dB]
    - DEC: 0 para detector, 1 para corrector
    """
    nombre = 'detector' if DEC == 0 else 'corrector'

    EbN0_db = np.asarray(EbN0_db)
    Gc = np.asarray(Gc)

    plt.figure(figsize=(10, 5))
    plt.semilogy(EbN0_db, Gc, 'o-', label='Ganancia real $G_c$')
    plt.semilogy(EbN0_db, [Ga] * len(EbN0_db), 'r--',
                 label='Ganancia asintótica $G_a$')

    plt.xlabel('$E_b/N_0$ [dB]')
    plt.ylabel('Ganancia [dB]')
    plt.title(f'Ganancia del {nombre}')
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()

    # Crear carpeta de resultados si no existe
    res_dir = os.path.join(os.path.dirname(__file__), 'resultados')
    os.makedirs(res_dir, exist_ok=True)

    # Guardar el gráfico
    plt.savefig(os.path.join(res_dir, f'{nombre}_ganancia.png'))
    plt.show()


def crear_tabla(EbN0_values, P_ep, P_eb, Gc, Ga, DEC):
    # Create a dictionary with the data
    data = {
        'Eb/N0 [dB]': EbN0_values,
        'P_ep': P_ep,
        'P_eb': P_eb,
        'Gc': Gc,
        'Ga': [Ga] * len(EbN0_values)  # Repeat Ga value for each row
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # Format the DataFrame to display with 6 decimal places for probabilities
    pd.set_option('display.float_format', lambda x: '%.6f' % x)

    # Create resultados directory if it doesn't exist
    res_dir = os.path.join(os.path.dirname(__file__), 'resultados')
    os.makedirs(res_dir, exist_ok=True)

    # Guardar la tabla en un archivo CSV
    nombre = "detector" if DEC == 0 else "corrector"
    df.to_csv(os.path.join(res_dir, f'{nombre}_tabla.csv'), index=False)
