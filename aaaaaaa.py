import random

# Lista de jugadores
jugadors = [
    {"nom": "Bargos", "diners": 300, "fitxes": {"5": 2, "10": 2, "20": 1, "50": 1, "100": 0}, "aposta": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36], "color": (255, 128, 0)},
    {"nom": "Cachi", "diners": 200, "fitxes": {"5": 2, "10": 2, "20": 1, "50": 1, "100": 0}, "aposta": [], "color": (204, 169, 221)},
    {"nom": "Albert", "diners": 100, "fitxes": {"5": 2, "10": 2, "20": 1, "50": 1, "100": 0}, "aposta": [], "color": (50, 120, 200)}
]

# Valores de las fichas en centavos (ordenados de mayor a menor)
denominacions = [100, 50, 20, 10, 5]

def distribuir_fitxes(jugadors, denominacions):
    for jugador in jugadors:
        diners_restants = jugador["diners"]

        # Reinicia las fichas del jugador
        for valor in denominacions:
            jugador["fitxes"][str(valor)] = 0

        # Garantiza al menos una de cada denominación más pequeña (excepto 100)
        for valor in denominacions:
            if valor != 100 and diners_restants >= valor:
                jugador["fitxes"][str(valor)] += 1
                diners_restants -= valor

        # Si sobra dinero suficiente, añade una ficha de 100
        if diners_restants >= 100:
            jugador["fitxes"]["100"] += 1
            diners_restants -= 100

        # Distribuir el dinero restante respetando el orden de las denominaciones
        for valor in denominacions:
            while diners_restants >= valor:
                jugador["fitxes"][str(valor)] += 1
                diners_restants -= valor

    return jugadors
