import heapq
import numpy as np
import math
import itertools


class Nodo:
    def __init__(self, simbolo=None, prob=0.0):
        self.simbolo = simbolo
        self.prob = prob
        self.izq = None
        self.der = None

    def __str__(self):
        return self._str_aux(0)

    def _str_aux(self, nivel):
        indent = "  " * nivel
        if self.simbolo is not None:
            return f"{indent}{self.simbolo}: {self.prob:.6f}\n"
        else:
            resultado = f"{indent}Prob: {self.prob:.6f}\n"
            if self.izq:
                resultado += self.izq._str_aux(nivel + 1)
            if self.der:
                resultado += self.der._str_aux(nivel + 1)
            return resultado


def huffman(simbolos: list, probabilidades: list) -> Nodo:
    """
    Construye un árbol de Huffman utilizando una heap.

    Inputs:
        - simbolos: Lista de símbolos.
        - probabilidades: Lista de probabilidades asociadas a cada símbolo.

    Output:
        - Nodo raíz del árbol de Huffman construido.
    """
    if not simbolos or not probabilidades or len(simbolos) != len(probabilidades):
        raise ValueError(
            "Req: listas no vacías y con la misma longitud.")

    # Caso especial: un solo símbolo
    if len(simbolos) == 1:
        return Nodo(simbolos[0], probabilidades[0])

    # Heap denodos según su probabilidad
    heap = []  # (probabilidad, es_hoja, contador, nodo)
    contador = 0

    for s, p in zip(simbolos, probabilidades):
        # Cada símbolo(s) y su probabilidad(p) se colocan en el heap como una tupla
        nodo = Nodo(s, p)
        heap.append((p, 1, contador, nodo))  # es_hoja = 1 para hojas
        contador += 1  # contador para romper empates

    # heapify convierte la lista en un heap válido.
    heapq.heapify(heap)

    while len(heap) > 1:
        # Los dos nodos con menor probabilidad
        p1, _, _, n1 = heapq.heappop(heap)
        p2, _, _, n2 = heapq.heappop(heap)

        # Nuevo nodo -> p1 + p2
        nuevo = Nodo(None, p1 + p2)
        nuevo.izq = n1
        nuevo.der = n2

        # Nuevo nodo al heap:
        # es_hoja = 0  -> nodo interno
        heapq.heappush(heap, (nuevo.prob, 0, contador, nuevo))
        contador += 1

    return heap[0][3]  # Devuelve la raíz


def codificar(arbol: Nodo) -> dict:
    """
    Recorre recursivamente el árbol de Huffman.
    Asigna 0 a la izquierda y 1 a la derecha.
    Si el árbol sólo tiene un símbolo, se le asigna "0" por convención.

    Inputs:
        - arbol: Árbol de Huffman
        - simbolos: Lista de símbolos
        - probabilidades: Lista de probabilidades asociadas a los símbolos

    Outputs:
        - codigos: Diccionario con los códigos de cada símbolo ordenados por largo
        - largo_promedio: Largo promedio de los códigos ponderados por probabilidad
        - entropia: Entropía de la fuente
    """
    codigos = {}

    def aux(nodo, prefijo):
        if nodo.izq is None and nodo.der is None:
            codigos[nodo.simbolo] = prefijo if prefijo else "0"
        else:
            aux(nodo.izq, prefijo + "0")
            aux(nodo.der, prefijo + "1")

    aux(arbol, "")

    # Ordenar codigos por largo (para visualizar)
    codigos = dict(sorted(codigos.items(), key=lambda x: len(x[1])))

    return codigos


def extender_fuente(simbolos: list, probabilidades: list, n: int) -> tuple[list, list]:
    """
    Genera la fuente binaria extendida de orden n. 
    Cada símbolo extendido es una tupla de longitud n tomada
    del producto cartesiano de 'simbolos'. Su probabilidad es el
    producto de las prob. individuales.

    Inputs:
        - simbolos: lista de símbolos originales (ej. [0,1] o ["A","B","C"])
        - probabilidades: lista de probabilidades asociadas a cada símbolo
        - n: orden de extensión (n >= 1)

    Output:
        - (simbolos_ext, probabilidades_ext)
          · simbolos_ext: lista de tuplas de longitud n
          · probabilidades_ext: lista de floats, probabilidad de cada símbolo extendido
    """
    if n < 1:
        raise ValueError("El orden debe ser >= 1")

    # Mapear cada símbolo a su probabilidad
    prob_dict = dict(zip(simbolos, probabilidades))

    # Producto cartesiano para generar todas las secuencias de longitud n
    combinaciones = itertools.product(simbolos, repeat=n)

    simbolos_ext = []
    probabilidades_ext = []

    for tupla in combinaciones:
        p = 1.0
        for s in tupla:
            p *= prob_dict[s]
        simbolos_ext.append(tuple(tupla))
        probabilidades_ext.append(p)

    return simbolos_ext, probabilidades_ext
