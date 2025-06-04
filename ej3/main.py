import os
from proc_imagen import procesar_imagen
from huffman import extender_fuente, huffman, codificar
import math


def main():
    path = os.path.join(os.path.dirname(__file__), "logo_FI.tif")

    # Procesar imagen
    n = 3
    # Generar simbolos de 3 bits
    simbolos = [f"{i:0{n}b}" for i in range(2**n)]
    # Procesar imagen y obtener probabilidades de cada simbolo
    probabilidades = procesar_imagen(path, simbolos)

    print(">>> Fuente original:")
    for s, p in zip(simbolos, probabilidades):
        print(f"  {s}: {p:.4f}")

    # Extender fuente orden 2
    simbolos_ext_2, probabilidades_ext_2 = extender_fuente(
        simbolos, probabilidades, 2)

    print(">>> Fuente extendida (orden 2):")
    for s, p in zip(simbolos_ext_2, probabilidades_ext_2):
        print(f"  {s} → {p:.4f}")

    # Codificar fuente extendida de orden 2
    arbol_ext2 = huffman(simbolos_ext_2, probabilidades_ext_2)
    print(arbol_ext2)
    codigos_ext2 = codificar(arbol_ext2)

    # Crear diccionario de probabilidades para los símbolos extendidos
    prob_dict = dict(zip(simbolos_ext_2, probabilidades_ext_2))

    # Calcular largo promedio
    largo_promedio = sum(
        prob_dict[s] * len(codigos_ext2[s]) for s in codigos_ext2)
    # Entropía
    entropia = -sum(
        prob_dict[s] * math.log2(prob_dict[s]) for s in codigos_ext2 if prob_dict[s] > 0)

    print(f"Largo promedio: {largo_promedio}")
    print(f"Entropía: {entropia}")

    print(">>> Codigos extendida (orden 2):")
    for s, c in codigos_ext2.items():
        print(f"  {s}: {c} {len(c), prob_dict[s]}")


if __name__ == "__main__":
    main()
