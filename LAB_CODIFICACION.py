import numpy as np
import math
import matplotlib
import heapq
import pandas as pd
import collections
from collections import defaultdict

pixel_values = [128, 75, 72, 105, 149, 169, 127, 100,
           122, 84, 83, 84, 146, 138, 142, 139,
           118, 98, 89, 94, 136, 96, 143, 188,
           122, 106, 79, 115, 148, 102, 127, 167,
           127, 115, 106, 94, 155, 124, 103, 155,
           125, 115, 130, 140, 170, 174, 115, 136,
           127, 110, 122, 163, 175, 140, 119, 87,
           146, 114, 127, 140, 131, 142, 153, 93]

contador = {}
num_valores_unicos = 0

# Contar cuántas veces aparece cada valor
for valor in pixel_values:
    if valor in contador:
        contador[valor] += 1
    else:
        contador[valor] = 1

# Contar cuántos valores se repiten solo una vez
for clave, valor in contador.items():
    if valor == 1:
        num_valores_unicos += 1

print("Número de valores que se repiten solo una vez:", num_valores_unicos)


prob_dict = defaultdict(list)
total_pixels = len(pixel_values)

for p in set(pixel_values):
    prob = pixel_values.count(p) / total_pixels
    prob_dict[prob].append(p)

for prob, pixel_group in sorted(prob_dict.items(), reverse=True):
    print(f"Pixel(es): {pixel_group}")
    print(f"Probabilidad: {prob:.4f}")
    print ()

# Conteo de ocurrencias de cada símbolo
symbol_counts = collections.Counter(pixel_values)

# Cálculo de la probabilidad de cada símbolo
total_symbols = sum(symbol_counts.values())
symbol_probabilities = {symbol: count / total_symbols for symbol, count in symbol_counts.items()}

print(symbol_probabilities)

def shannon_fano(probabilities):
    if len(probabilities) == 1:
        return {list(probabilities.keys())[0]: '0'}

    # Ordena los símbolos por probabilidad en orden descendente
    sorted_probabilities = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)

    # Divide los símbolos en dos grupos de aproximadamente igual probabilidad
    group_1 = dict(sorted_probabilities[:len(sorted_probabilities) // 2])
    group_2 = dict(sorted_probabilities[len(sorted_probabilities) // 2:])

    # Genera los códigos recursivamente para cada grupo y los concatena con "0" y "1" respectivamente
    codes = {}
    for symbol, code_prefix in shannon_fano(group_1).items():
        codes[symbol] = '0' + code_prefix
    for symbol, code_prefix in shannon_fano(group_2).items():
        codes[symbol] = '1' + code_prefix

    return codes

# Genera los códigos para cada símbolo
codes = shannon_fano(symbol_probabilities)

# Convierte los diccionarios en objetos de la serie pandas.Series
symbol_probs_series = pd.Series(symbol_probabilities, name='Probabilidad')
codes_series = pd.Series(codes, name='Código')

# Combina las series en un marco de datos
df = pd.concat([symbol_probs_series, codes_series], axis=1)

# Ordena las filas por orden descendente de probabilidad
df.sort_values(by='Probabilidad', ascending=False, inplace=True)
print("\n\nALGORTIMO DE SHANNON FANO\n")
print(df)

#Para huffman
print("\n\nALGORTIMO DE HUFFMAN\n")

def calculate_frequencies(symbol_sequence):
    symbol_counts = collections.Counter(symbol_sequence)
    total_symbols = sum(symbol_counts.values())
    symbol_probabilities = {symbol: count / total_symbols for symbol, count in symbol_counts.items()}
    return symbol_probabilities


def huffman_encoding(symbol_sequence):
    symbol_probabilities = calculate_frequencies(symbol_sequence)

    heap = [[probability, [symbol, '']] for symbol, probability in symbol_probabilities.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        low_prob = heapq.heappop(heap)
        high_prob = heapq.heappop(heap)

        for pair in low_prob[1:]:
            pair[1] = '0' + pair[1]
        for pair in high_prob[1:]:
            pair[1] = '1' + pair[1]

        merged_pairs = low_prob[1:] + high_prob[1:]
        heapq.heappush(heap, [low_prob[0] + high_prob[0]] + merged_pairs)

    codes = {symbol: code for symbol, code in heap[0][1:]}
    return codes

# Calcula los códigos de Huffman para la secuencia de símbolos
huffman_codes = huffman_encoding(pixel_values)

# Muestra los resultados en una tabla
print('Símbolo\t\tProbabilidad\tHuffman')
for symbol, probability in calculate_frequencies(pixel_values).items():
    print(f"{symbol}\t\t{probability:.4f}\t\t{huffman_codes[symbol]}")


# Conteo de ocurrencias de cada símbolo
symbol_counts = collections.Counter(pixel_values)

# Cálculo de la probabilidad de cada símbolo
total_symbols = sum(symbol_counts.values())
symbol_probabilities = {symbol: count / total_symbols for symbol, count in symbol_counts.items()}

# Cálculo de la entropía de Shannon
entropy = sum(p * math.log2(1/p) for p in symbol_probabilities.values())

print(f"La entropía de Shannon de la lista de pixeles es {entropy:.4f}")

def huffman_encoding(symbol_sequence):
    symbol_probabilities = calculate_frequencies(symbol_sequence)

    heap = [[probability, [symbol, '']] for symbol, probability in symbol_probabilities.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        low_prob = heapq.heappop(heap)
        high_prob = heapq.heappop(heap)

        for pair in low_prob[1:]:
            pair[1] = '0' + pair[1]
        for pair in high_prob[1:]:
            pair[1] = '1' + pair[1]

        merged_pairs = low_prob[1:] + high_prob[1:]
        heapq.heappush(heap, [low_prob[0] + high_prob[0]] + merged_pairs)

    codes = {symbol: code for symbol, code in heap[0][1:]}
    return codes

# Calcula los códigos de Huffman para la secuencia de símbolos
huffman_codes = huffman_encoding(pixel_values)

# Muestra los resultados en una tabla
print('Símbolo\t\tProbabilidad\tHuffman')
for symbol, probability in calculate_frequencies(pixel_values).items():
    print(f"{symbol}\t\t{probability:.4f}\t\t{huffman_codes[symbol]}")


# Conteo de ocurrencias de cada símbolo
symbol_counts = collections.Counter(pixel_values)

# Cálculo de la probabilidad de cada símbolo
total_symbols = sum(symbol_counts.values())
symbol_probabilities = {symbol: count / total_symbols for symbol, count in symbol_counts.items()}

# Cálculo de la entropía de Shannon
entropy = sum(p * math.log2(1/p) for p in symbol_probabilities.values())

print(f"La entropía de Shannon de la lista de pixeles es {entropy:.4f}")