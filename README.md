# TIC - TRABAJO PRÁCTICO DE SIMULACIÓN

Autor: Santiago Nihany

Legajo: 03012/3

Entrega: 30/05/2025

---

### Transmisión digital

Este proyecto implementa la simulación de un sistema de comunicación digital sobre un canal AWGN, incorporando codificación de fuente y canal.

#### Objetivos

- Simular un sistema de transmisión binaria con modulación BPSK sobre canal AWGN.

- Implementar codificación de canal utilizando un código de bloque lineal (14,10) sistemático con detección dura.

- Evaluar el desempeño con y sin codificación mediante curvas de tasa de error.

- Calcular y analizar la ganancia de codificación.

Como correrlo:

```bash
python ej1/main.py
```

### Compresión

Se realiza la compresión de un archivo de imagen binaria mediante la construcción de árboles de Huffman para fuentes extendidas de orden 2 y 3.

#### Objetivos

- Implementar codificación de fuente mediante el algoritmo de Huffman (fuente extendida de orden 2 y 3).

- Analizar la eficiencia de compresión en función de la estructura estadística del archivo de entrada('logo FI.tif').
