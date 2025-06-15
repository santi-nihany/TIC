import os
import math
import pandas as pd
from proc_imagen import procesar_imagen
from huffman import extender_fuente, huffman, codificar


def main():
    path = os.path.join(os.path.dirname(__file__), "logo_FI.tif")
    resultados = []

    for n in range(1, 4):  # n = 1, 2, 3
        # Fuente original simbolos largo n
        simbolos = [f"{i:0{n}b}" for i in range(2**n)]
        probabilidades = procesar_imagen(path, simbolos)
        print(f"\nFuente original (longitud de símbolo n = {n} bits):")
        print("Probabilidades de símbolos originales:")
        for s, p in zip(simbolos, probabilidades):
            print(f"  {s}: {p:.6f}")

        for orden in (2, 3):
            # Extensión de fuente
            simbolos_ext, probabilidades_ext = extender_fuente(
                simbolos, probabilidades, orden)
            arbol = huffman(simbolos_ext, probabilidades_ext)
            codigos = codificar(arbol)
            prob_dict = dict(zip(simbolos_ext, probabilidades_ext))

            # Cálculos
            entropia = -sum(p * math.log2(p)
                            for p in probabilidades_ext if p > 0)
            largo_promedio = sum(
                prob_dict[s] * len(codigos[s]) for s in codigos)
            tasa_compresion = (orden * n) / \
                largo_promedio if largo_promedio > 0 else 0

            resultados.append({
                "n": n,
                "Orden": orden,
                "Largo promedio (bits)": largo_promedio,
                "Entropía (bits/símbolo)": entropia,
                "Tasa compresión": tasa_compresion
            })

            print(f"=== Fuente extendida orden {orden} ===")
            print(f"Largo promedio (bits): {largo_promedio:.6f}")
            print(f"Entropía (bits/símbolo): {entropia:.6f}")
            print(f"Tasa de compresión: {tasa_compresion:.6f}")

    # Resultados .csv
    df = pd.DataFrame(resultados)
    csv_path = os.path.join(os.path.dirname(__file__), "resultados.csv")
    df.to_csv(csv_path, index=False, float_format="%.6f")


if __name__ == "__main__":
    main()
