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
    for jugador in j.jugadors:  # Cambiado de j.jugadors a jugadors
        apuesta_jugador = jugador["aposta"]
        tipus = jugador["tipus"]

        if tipus in especials:
            print(f"Jugador {jugador['nom']} del tipus {tipus} ha apostat {apuesta_jugador}")
            repartir_premis_especials(num, tipus, jugador)
        else:
            print(f"Jugador {jugador['nom']} del tipus: {tipus} ha apostado: {apuesta_jugador}")
            repartir_premis(num, jugador)



def obtener_valores_apuestas(num,apuestas,banca):
    total = 0
    for apuesta in apuestas:
        total += apuesta['value']
    if num not in apuestas:
            banca['diners'] += total
def repartir_premis_especials(num, tipus, jugador):
    aposta = jugador["aposta"]

    if tipus == "BLACK":
        numeros_negros = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        if num in numeros_negros:
            premio = sum(aposta) * 2  #Valores provisionales
            jugador["diners"] += premio
            print(f"{jugador['nom']} ha ganado {premio} con su apuesta BLACK.")
        else:
            print(f"{jugador['nom']} ha perdido con su apuesta BLACK.")

    elif tipus == "RED":
        numeros_rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        if num in numeros_rojos:
            premio = sum(aposta) * 2
            jugador["diners"] += premio
            print(f"{jugador['nom']} ha ganado {premio} con su apuesta RED.")

    elif tipus == "PAR":
        if num % 2 == 0:
            premio = sum(aposta) * 2
            jugador["diners"] += premio
            print(f"{jugador['nom']} ha ganado {premio} con su apuesta PAR.")
    elif tipus == "IMP":
        if num % 2 != 0:
            premio = sum(aposta) * 2
            jugador["diners"] += premio
            print(f"{jugador['nom']} ha ganado {premio} con su apuesta IMP.")
    elif tipus == "2to1":
         if num in t.betting_table[0]:
            premio += 2
            jugador["diners"] += premio
    elif tipus == "2to2":
         if num in t.betting_table[1]:
            premio += 2
            jugador["diners"] += premio
    elif tipus == "2to3":
         if num in t.betting_table[2]:
            premio += 2
            jugador["diners"] += premio
    elif tipus == "0":
         if 0 in aposta:
              premio += 4
              jugador["diners"] +=premio
    


def repartir_premis(num, jugador):
    """Maneja premios para apuestas no especiales."""
    aposta = jugador["aposta"]

    # Verificar si aposta está vacía o no es válida
    if not aposta or not isinstance(aposta, list):
        print(f"{jugador['nom']} no ha realizado ninguna apuesta válida.")
        return

    # Suponiendo que la apuesta contiene números específicos (y si no es así, se puede ajustar)
    if num in aposta:
        premio = sum(aposta) * 36  # Paga 36x el monto apostado
        jugador["diners"] += premio
        print(f"{jugador['nom']} ha ganado {premio} con su apuesta directa.")
    else:
        print(f"{jugador['nom']} ha perdido con su apuesta directa.")


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