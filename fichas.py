import math
import pygame
import sys
import utils
import jugadors as j
import jugadors_dades as jd
import tauler as t
# Inicialización de Pygame y configuración de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

def gestionar_especials(label, aposta_jugador):
    negres = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    vermells = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

    parells = []
    imparells = []
    for i in range(1,37):
        if i % 2 == 0:
            parells.append(i)
        else:
            imparells.append(i)

    if label == "BLACK":
        for negre in negres:
            if negre not in aposta_jugador:
                aposta_jugador.append(negre)
    elif label == '0':
        aposta_jugador.append(0)
    elif label == "RED":
        for vermell in vermells:
            if vermell not in aposta_jugador:
                aposta_jugador.append(vermell)
    elif label == "PAR": 
        for parell in parells:
            if parell not in aposta_jugador:
                aposta_jugador.append(parell)
    elif label == "IMP":  # Números impares
        for imparell in imparells:
            if imparell not in aposta_jugador:
                aposta_jugador.append(imparell)
    elif label == "2 to 1":
        for num in t.betting_table[0]:
            if num not in aposta_jugador:
                aposta_jugador.append(num)
    elif label == "2 to 2":
        for num in t.betting_table[1]:
            if num not in aposta_jugador:
                aposta_jugador.append(num)
    elif label == "2 to 3":
        for num in t.betting_table[2]:
            if num not in aposta_jugador:
                aposta_jugador.append(num)


    print(aposta_jugador)