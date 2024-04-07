
import numpy as np
from math import log
import heapq
rojo=3
amarillo=2
azul=1
verde=4
naranja=5
# Definir la matriz
matriz = np.array([[rojo,amarillo,azul,verde,rojo,verde],
                   [azul,naranja,azul,amarillo,verde,rojo],
                   [amarillo,naranja,rojo,azul,amarillo,amarillo],
                   [verde,azul,naranja,rojo,azul,verde],
                   [azul,rojo,amarillo,azul,verde,azul],
                   [naranja,naranja,azul,amarillo,azul,naranja]])

lista_p=[]





#Hallar M
M=len(np.unique(matriz))
# Definir el valor específico que se desea encontrar
valor_especifico = [azul,amarillo,rojo,verde,naranja]

count=1

print("El M seria:",M)
print("M---Pi--Información")
for x in  valor_especifico:

# Contar el número de veces que el valor ocurre en la matriz y dividir por el número total de elementos de la matriz
     probabilidad_ocurrencia = np.count_nonzero(matriz == x) / matriz.size
     lista_p.append(round(probabilidad_ocurrencia,2))
     informacion=log((1/round(probabilidad_ocurrencia,2)),2)
     print(count,"----",round(probabilidad_ocurrencia,2),"----",round(informacion,2))
     count=count+1




def shannon_fano_code(symbols, probabilities):
    """
    Implementación del algoritmo de codificación de Shannon-Fano.

    :param symbols: lista de símbolos.
    :param probabilities: lista de probabilidades correspondientes a los símbolos.
    :return: un diccionario que mapea los símbolos a sus códigos de Shannon-Fano correspondientes.
    """
    # Combinar los símbolos y las probabilidades en una lista de tuplas.
    tuples = list(zip(symbols, probabilities))

    # Ordenar la lista de tuplas en orden descendente según las probabilidades.
    tuples.sort(key=lambda x: x[1], reverse=True)

    # Implementar la codificación de Shannon-Fano recursivamente.
    def shannon_fano_rec(tuples):
        if len(tuples) == 1:
            return {tuples[0][0]: '0'}
        else:
            split_index = 1
            cum_prob = tuples[0][1] - tuples[1][1]
            while abs(cum_prob) > abs(tuples[0][1] - sum([x[1] for x in tuples[:split_index + 1]])):
                split_index += 1
                cum_prob = tuples[0][1] - sum([x[1] for x in tuples[:split_index]])

            # Recursivamente llamar a la función para las dos mitades de la lista.
            dict1 = shannon_fano_rec(tuples[:split_index])
            dict2 = shannon_fano_rec(tuples[split_index:])

            # Asignar '0' a la primera mitad y '1' a la segunda mitad.
            for key in dict1:
                dict1[key] = '0' + dict1[key]
            for key in dict2:
                dict2[key] = '1' + dict2[key]

            # Combinar los dos diccionarios resultantes.
            dict1.update(dict2)
            return dict1

    # Llamar a la función recursiva y devolver el diccionario resultante.
    return shannon_fano_rec(tuples)


print("Velocidad de Información:",round(64000*log(M,2)))
print("Frecuencia Binaria:",round(64000*2.36))
print()


diccionario_1=shannon_fano_code(valor_especifico,lista_p)

print("Algoritmo de shannon",diccionario_1)
