#!/usr/bin/env python3

import pygame
import sys
import utils
import random
import tauler as t
import jugadors as j
import jugadors_dades as jd
import fichas as f
import historial as h

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
MARRON = (151, 91, 57)
GOLD = (255, 215, 0)
CENICA = (138, 149, 151)
VERDE = (0, 100, 0)
circulo_ruleta = pygame.image.load("circuloruleta.png")
fondo = pygame.image.load("casinofondo.png")
buen_fondo = pygame.transform.scale(fondo, (860, 680))

pygame.init()
clock = pygame.time.Clock()
historial_ganador = []
historial_complet = []
rule = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
angulo_actual = 265
girando = False
angulo_velocidad = 0
seleccionado = None
idx = 0
apostar = False

# Definir la finestra
screen = pygame.display.set_mode((860, 680))
pygame.display.set_caption('Ruleta')
mouse = {'x': -1, 'y': -1}
font = pygame.font.SysFont("Arial", 22)

# Definir botones
buttons = [
    {'name': 'Girar', 'x': 500, 'y': 400, 'width': 100, 'height': 50, 'pressed': False},
    {'name': 'Apostar', 'x': 650, 'y': 400, 'width': 100, 'height': 50, 'pressed': False},
    {'name': 'Log', 'x': 650, 'y': 250, 'width': 100, 'height': 50, 'pressed': False}
]

# Lista de números rojos y negros
RED_NUMBERS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
BLACK_NUMBERS = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

# Clase para jugadores
class Jugador:
    def __init__(self, nombre, fichas):
        self.nombre = nombre
        self.fichas = fichas
        self.apuestas = []  # Lista de apuestas hechas por el jugador

    def agregar_apuesta(self, tipo_apuesta, cantidad):
        self.apuestas.append((tipo_apuesta, cantidad))

    def limpiar_apuestas(self):
        self.apuestas = []  # Limpiar las apuestas al finalizar la ronda

# Crear jugadores
jugadores = [Jugador("Jugador 1", 1000), Jugador("Jugador 2", 1000)]

# Función principal
def main():
    global idx, apostar
    is_looping = True

    while is_looping:
        is_looping = app_events()  # Procesar eventos (clics, etc.)
        app_run()  # Ejecutar la lógica del juego (giro de ruleta, actualizaciones)
        app_draw()  # Dibujar el estado actual del juego en la pantalla

        clock.tick(60)  # Limitar a 60 FPS

    # Fuera del bucle, cerrar la aplicación
    pygame.quit()
    sys.exit()

# Función para girar la ruleta
def girar_ruleta():
    global angulo_actual, angulo_velocidad, girando, seleccionado
    if girando:
        # Actualizar el ángulo actual
        angulo_actual += angulo_velocidad
        angulo_actual %= 360  # Pa que el ángulo no se pase de 360.
        angulo_velocidad *= 0.98  # Baja la velocidad de forma suave

        if angulo_velocidad < 0.5:
            girando = False
            angulo_velocidad = 0

            # El número ganador
            flecha_angulo = (270 - angulo_actual) % 360
            segmento = int(flecha_angulo // (360 / len(rule)))
            seleccionado = rule[segmento]
            h.gestionar_nums(historial_ganador, seleccionado)
            print(f"Seleccionado: {seleccionado}")

            # Verificar apuestas para cada jugador
            for jugador in jugadores:
                ganancia = verificar_apuestas(jugador, seleccionado)
                if ganancia > 0:
                    print(f"{jugador.nombre} ganó {ganancia} fichas!")
                    jugador.fichas += ganancia  # Actualizamos las fichas
                else:
                    print(f"{jugador.nombre} perdió su apuesta.")
                
                jugador.limpiar_apuestas()  # Limpiar las apuestas del jugador después de la ronda

# Función para verificar las apuestas de un jugador
def verificar_apuestas(jugador, numero_ganador):
    ganancias = 0
    for apuesta in jugador.apuestas:
        tipo, cantidad = apuesta

        if tipo == "Rojo" and numero_ganador in RED_NUMBERS:  # Apuesta a rojo
            ganancias += cantidad
        elif tipo == "Negro" and numero_ganador in BLACK_NUMBERS:  # Apuesta a negro
            ganancias += cantidad
        elif tipo == "Par" and numero_ganador % 2 == 0:  # Apuesta a par
            ganancias += cantidad
        elif tipo == "Impar" and numero_ganador % 2 != 0:  # Apuesta a impar
            ganancias += cantidad
        elif tipo == "Numero" and numero_ganador == apuesta[1]:  # Apuesta exacta al número
            ganancias += cantidad * 36  # Ganancia por acertar el número exacto
    return ganancias

# Gestionar eventos
def app_events():
    global mouse, angulo_actual, girando, angulo_velocidad, seleccionado, apostar, idx
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEMOTION:
            mouse['x'], mouse['y'] = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if utils.is_point_in_rect(mouse, button) and not girando and button['name'] == "Girar":
                    girando = True
                    angulo_velocidad = random.randint(5, 37)  # Velocidad random
                    print("¡Girando!")
                elif utils.is_point_in_rect(mouse, button) and not girando and button['name'] == "Apostar":
                    apostar = True
                    print("Apuesta hecha!")
                    idx = jd.gestio_turns(screen, font, j.jugadors, idx, apostar)  # Cambio de jugador 
                    apostar = False
            for button in t.betting_buttons:
                if utils.is_point_in_rect(mouse, button):
                    print(f"button {button['number']}!")
                    tipo_apuesta = button['label']  # Tipo de apuesta
                    cantidad = 10  # Cantidad predeterminada para la apuesta (puede cambiar)
                    jugadores[idx].agregar_apuesta(tipo_apuesta, cantidad)  # Registra la apuesta del jugador
            for button_apostar in t.custom_buttons:
                if utils.is_point_in_rect(mouse, button_apostar):
                    print(f"Custom Button {button_apostar.get('label', 'RED/BLACK')} clicked!")  # Handle custom button click here

    girar_ruleta()  

    return True

# Función de la aplicación en ejecución (actualizar la lógica de turnos si es necesario)
def app_run(): 
    pass  

# Función para dibujar la ruleta
def dibujar_ruleta():
    center = {"x": 300, "y": 250}

    for i, casella in enumerate(rule):
        inici_angle = (360 / 37) * i  # Ángulo inicial para dibujar cada casilla
        fi_angle = (360 / 37) * (i + 1)  # Ángulo final

        # PUNTOS DEL POLÍGONO (CÍRCULO GRANDE)
        p0 = utils.point_on_circle(center, 100, inici_angle + angulo_actual)
        p1 = utils.point_on_circle(center, 150, inici_angle + angulo_actual)
        p2 = utils.point_on_circle(center, 150, fi_angle + angulo_actual)
        p3 = utils.point_on_circle(center, 100, fi_angle + angulo_actual)

        # COLORES DE LA RULETA
        if i == 0:  
            color = GREEN
        elif i % 2 == 1: 
            color = RED
        else:  
            color = BLACK       

        # DICCIONARIOS CON COORDENADAS
        points = [  # CÍRCULO GRANDE
            (int(p0["x"]), int(p0["y"])),
            (int(p1["x"]), int(p1["y"])),
            (int(p2["x"]), int(p2["y"])),
            (int(p3["x"]), int(p3["y"]))
        ]

        # DIBUJAR FLECHA
        coords_flecha = [
            (300 - 10, 80),
            (300 + 10, 80),
            (300, 105)
        ]
        pygame.draw.polygon(screen, BLUE, coords_flecha)
        pygame.draw.polygon(screen, BLACK, coords_flecha, 2)

        # Dibujar los polígonos
        pygame.draw.polygon(screen, color, points)

        # Dibujar el número en el centro de cada casilla
        centre_quesito = utils.point_on_circle(center, 140, (inici_angle + fi_angle) / 2 + angulo_actual)
        fontnum = pygame.font.SysFont("Arial", 15)
        if color == BLACK:
            color_num = WHITE
        else:
            color_num = BLACK   

        txt = fontnum.render(str(casella), True, color_num)
        screen.blit(txt, (int(centre_quesito["x"] - txt.get_width() / 2), int(centre_quesito["y"] - txt.get_height() / 2)))  # Dibujar el número en cada casilla

# Función para dibujar el historial de los ganadores
def app_draw():
    # Pintar el fondo de blanco
    screen.fill(WHITE)
    screen.blit(buen_fondo, (0, 0))  # Fondo de la ruleta
    utils.draw_grid(pygame, screen, 50)  # Dibujar la cuadrícula

    t.draw_custom_buttons(screen)  # Botones personalizados
    t.draw_betting_buttons(screen)  # Botones de apuesta

    # Mostrar los jugadores
    jd.gestio_turns(screen, font, j.jugadors, idx, apostar)  # Muestra los turnos de los jugadores
    pygame.draw.circle(screen, CENICA, (300, 250), 100)  # Dibujar el círculo central

    screen.blit(circulo_ruleta, (230, 180))  # Imagen de la ruleta

    # Dibujar los círculos adicionales para decoración
    pygame.draw.circle(screen, GOLD, (300, 250), 100, 5)
    pygame.draw.circle(screen, GOLD, (300, 250), 70, 5)
    pygame.draw.circle(screen, GOLD, (300, 250), 154, 5)

    dibujar_ruleta()  # Dibujar la ruleta

    for button in buttons:
        text_girar = font.render(buttons[0]["name"], True, WHITE)
        text_apostar = font.render(buttons[1]["name"], True, WHITE)
        text_log = font.render(buttons[2]["name"], True, WHITE)
        pygame.draw.rect(screen, MARRON, (button["x"], button["y"], button["width"], button["height"]))  # Botón de giro
        pygame.draw.rect(screen, BLACK, (button["x"], button["y"], button["width"], button["height"]), 5)  # Botón de apuesta
        screen.blit(text_girar, (525, 415))
        screen.blit(text_apostar, (665, 415))
        screen.blit(text_log, (680, 265))

    h.mostrar_guanyadors(screen, seleccionado, historial_ganador)  # Mostrar historial
    f.afegir_fitxes(idx)  # Añadir fichas
    f.dibuixar_fitxes(screen)  # Dibujar fichas

    pygame.display.update()  # Actualizar la pantalla

if __name__ == "__main__":
    main()
