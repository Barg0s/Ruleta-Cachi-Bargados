import math
import pygame
import sys
import utils
import jugadors as j
import jugadors_dades as jd
import tauler as t
import random
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


def contar_fitxes(screen,idx):
    y = 400
    font = pygame.font.Font(None, 24)
    for key,value in j.jugadors[idx]["fitxes"].items():
        if value > 0:
            txt = font.render(f"X{str(value)}",True,WHITE)
            screen.blit(txt,(825,y))
            y += 60
def repartir_premis(num):
    for jugador in j.jugadors:
        aposta_jugador = jugador["aposta"]
        if num in aposta_jugador:
            jugador["diners"] +=35




def distribuir_fitxes(jugadors, valors_fitxes):
    for jugador in jugadors:
        diners_restants = jugador["diners"]
        jugador["fitxes"] = {}  # Reiniciar las fichas
        for valor in valors_fitxes:
            jugador["fitxes"][str(valor)] = 0

        # Si dinero < 100 mete fichas de cada
        for valor in valors_fitxes:
            if valor != 100 and diners_restants >= valor:
                jugador["fitxes"][str(valor)] += 1
                diners_restants -= valor

        # Si puede pos mete una de 100
        if diners_restants >= 100:
            jugador["fitxes"]["100"] += 1
            diners_restants -= 100

        # Fichas random
        while diners_restants > 0:
            for valor in valors_fitxes:
                if diners_restants >= valor:
                    jugador["fitxes"][str(valor)] += 1
                    diners_restants -= valor


def comprobar_aposta(num):
    especials = ["RED", "BLACK", "PAR", "IMP", "2to1", "2to2", "2to3"]
    for jugador in j.jugadors:
        apuesta_jugador = jugador["aposta"]
        print(f"Jugador {jugador['tipus']} ha apostado: {apuesta_jugador}")  
        repartir_premis(num) 


def gestionar_especials(idx,tipus):
    # Listas de números especiales
    negres = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    vermells = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    parells = [x for x in range(1, 37) if x % 2 == 0]
    imparells = [x for x in range(1, 37) if x % 2 != 0]

    # Verificar las apuestas de cada jugador
    aposta_jugador = j.jugadors[idx]["aposta"]
    if tipus == "BLACK":
            for num in negres:
                if num not in aposta_jugador: 
                    aposta_jugador.append(num)
    elif tipus == "RED":
            for num in vermells:
                if num not in aposta_jugador:
                    aposta_jugador.append(num) 
    elif tipus == "PAR":
            for num in parells:
                if num not in aposta_jugador:  
                    aposta_jugador.append(num) 
    elif tipus == "IMP":
            for num in imparells:
                if num not in aposta_jugador:  
                    aposta_jugador.append(num)  
    elif tipus == "2 to 1":
            for num in t.betting_table[0]:
                if num not in aposta_jugador:  
                    aposta_jugador.append(num)  
    elif tipus == "2 to 2":
            for num in t.betting_table[1]:
                if num not in aposta_jugador: 
                    aposta_jugador.append(num)  
    elif tipus == "2 to 3":
            for num in t.betting_table[2]:
                if num not in aposta_jugador:
                    aposta_jugador.append(num) 
    elif tipus == "0":
            if 0 not in aposta_jugador:  
                aposta_jugador.append(0)  

    print(aposta_jugador)