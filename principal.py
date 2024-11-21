#!/usr/bin/env python3

import pygame
import sys
import utils
import random
import tauler as t
import jugadors as j

import jugadors_dades as jd
# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 200)
RED = (255, 0, 0)  
GREEN = (0, 255, 0)
MARRON = (151, 91, 57)
GOLD = (255,215,0)
CENICA = (138,149,151)
VERDE = (0, 100, 0)
circulo_ruleta = pygame.image.load("circuloruleta.png")
fondo = pygame.image.load("casinofondo.png")
buen_fondo = pygame.transform.scale(fondo,(860,680))
pygame.init()
clock = pygame.time.Clock()
historial_ganador = []
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
font = pygame.font.SysFont("Arial",22)

# Definir botones
buttons = [
    {'name': 'Girar', 'x': 500, 'y': 400, 'width': 100, 'height': 50, 'pressed': False},
    {'name': 'Apostar', 'x': 650, 'y': 400, 'width': 100, 'height': 50, 'pressed': False}
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
            for button_apostar in t.custom_buttons:
                if utils.is_point_in_rect(mouse, button_apostar):
                    print(f"Custom Button {button_apostar.get('label', 'RED/BLACK')} clicked!")  # Handle custom button click here

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
# Dibujar
def app_draw():
    # Pintar el fondo de blanco

    screen.fill(WHITE)
    # Dibujar la cuadrícula
    screen.blit(buen_fondo,(0,0))
    utils.draw_grid(pygame, screen, 50)

    t.draw_custom_buttons(screen)
    t.draw_betting_buttons(screen)
    jd.gestio_turns(screen,font,j.jugadors,idx,apostar)
    pygame.draw.circle(screen,CENICA,(300,250),100)   

    screen.blit(circulo_ruleta, (230, 180))

    pygame.draw.circle(screen,GOLD,(300,250),100,5)    
    pygame.draw.circle(screen,GOLD,(300,250),70,5)
    pygame.draw.circle(screen,GOLD,(300,250),154,5)   

   
    dibujar_ruleta()

    for button in buttons:
        text_girar = font.render(buttons[0]["name"],True, WHITE)
        text_apostar = font.render(buttons[1]["name"],True, WHITE)
        pygame.draw.rect(screen, MARRON, (button["x"], button["y"], button["width"], button["height"])) #boton(provisional)
        pygame.draw.rect(screen, BLACK, (button["x"], button["y"], button["width"], button["height"]), 5) #boton(provisional)    screen.blit(text_girar,(525, 415))
        screen.blit(text_girar,(525, 415))
        screen.blit(text_apostar,(665, 415))

    mostrar_guanyadors()

    pygame.display.update()


def mostrar_guanyadors():
    # Actualizar la pantalla
    if seleccionado is not None:
        x = 430
        for num in historial_ganador: 
            texto_seleccion = font.render(f"{num},", True, BLACK)
            screen.blit(texto_seleccion, (x - texto_seleccion.get_width() // 2, 100))
            x += 35

if __name__ == "__main__":
    main()
