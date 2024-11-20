#!/usr/bin/env python3

import pygame
import sys
import utils
import random

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 200)
RED = (255, 0, 0)  
GREEN = (0, 255, 0)
MARRON = (75, 54, 33)

pygame.init()
clock = pygame.time.Clock()
historial_ganador = []
rule = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
angulo_actual = 265
girando = False
angulo_velocidad = 0
seleccionado = None
# Definir la finestra
screen = pygame.display.set_mode((860, 680))
pygame.display.set_caption('Ruleta')
mouse = {'x': -1, 'y': -1}

# Definir botones
buttons = [
    {'name': 'girar', 'x': 500, 'y': 400, 'width': 50, 'height': 50, 'pressed': False}
]

# Bucle de la aplicación
def main():
    is_looping = True

    while is_looping:
        is_looping = app_events()
        app_run()
        app_draw()

        clock.tick(60)  # Limitar a 60 FPS

    # Fuera del bucle, cerrar la aplicación
    pygame.quit()
    sys.exit()

def girar_ruleta():
    global angulo_actual, angulo_velocidad, girando, seleccionado
    if girando:
        # Actualizar el ángulo actual
        angulo_actual += angulo_velocidad
        angulo_actual %= 360  # pa que el angulo no se pase de 360.
        angulo_velocidad *= 0.98  # bajar la velocidad suave

        if angulo_velocidad < 0.5:
            girando = False
            angulo_velocidad = 0

            # El numero ganador
            flecha_angulo = (270 - angulo_actual) % 360 # averiguar donde esta la flecha
            segmento = int(flecha_angulo // (360 / len(rule))) #saber donde cayó la flecha( el // es para que divida a la baja)
            seleccionado = rule[segmento] #usa el segmento como index de la lista rule y pilla esa pos
            gestionar_nums(seleccionado)
            print(f"Seleccionado: {seleccionado}")


# Gestionar eventos
def app_events():
    global mouse, angulo_actual, girando, angulo_velocidad, seleccionado
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEMOTION:
            mouse['x'], mouse['y'] = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if utils.is_point_in_rect(mouse, buttons[0]) and not girando:
                girando = True
                angulo_velocidad = random.randint(1, 37)  # Velocidad random
                print("¡Girando!")

    girar_ruleta()  

    return True

def app_run(): 
    pass  

def gestionar_nums(num):
    historial_ganador.append(num)
    if len(historial_ganador) > 10:
        historial_ganador.pop(0)
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
            (300 - 10, 50),
            (300 + 10, 50),
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
def dibujar_historial():
    if seleccionado is not None:
        x = 430
        font = pygame.font.SysFont("Arial", 22)
        for num in historial_ganador:
            texto_seleccion = font.render(f"{num},", True, BLUE)
            screen.blit(texto_seleccion, (x - texto_seleccion.get_width() // 2, 100))
            x += 35
# Dibujar
def app_draw():
    # Pintar el fondo de blanco
    screen.fill(WHITE)
    # Dibujar la cuadrícula
    utils.draw_grid(pygame, screen, 50)

    # Dibujar las casillas de la ruleta
    dibujar_ruleta()
    pygame.draw.rect(screen, BLACK, (buttons[0]["x"], buttons[0]["y"], buttons[0]["width"], buttons[0]["height"]), 5) #boton(provisional)
    mostrar_guanyadors()

    pygame.display.update()


def mostrar_guanyadors():
    # Actualizar la pantalla
    if seleccionado is not None:
        x = 430
        font = pygame.font.SysFont("Arial",22)
        for num in historial_ganador:
            texto_seleccion = font.render(f"{num},", True, BLUE)
            screen.blit(texto_seleccion, (x - texto_seleccion.get_width() // 2, 100))
            x += 35

if __name__ == "__main__":
    main()
