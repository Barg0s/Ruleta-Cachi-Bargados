#!/usr/bin/env python3

import math
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import utils

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # Rojo
GREEN = (0, 255, 0)  # Verde

pygame.init()
clock = pygame.time.Clock()

# Definir la finestra
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Window Title')

# Bucle de l'aplicació
def main():
    is_looping = True

    while is_looping:
        is_looping = app_events()
        app_run()
        app_draw()

        clock.tick(60) # Limitar a 60 FPS

    # Fora del bucle, tancar l'aplicació
    pygame.quit()
    sys.exit()

# Gestionar events
def app_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Botó tancar finestra
            return False
    return True

# Fer càlculs
def app_run():
    pass

# Dibuixar
def app_draw():
    
    # Pintar el fons de blanc
    screen.fill(WHITE)

    # Dibuixar la graella
    utils.draw_grid(pygame, screen, 50)

    # Dibuixar les dades
    center = {"x": 300, "y": 250}
    
    coords = [
        ((240),(250)),
        ((250),(275)),
        ((260),(250))

    ]
    pygame.draw.polygon(screen,BLACK,coords,3)

    # Dividir el círculo en 37 partes
    pygame.draw.circle(screen,(255,0,0),(center["x"],center["y"]),5,5)

    # Actualizar el dibujo en la ventana
    pygame.display.update()

if __name__ == "__main__":
    main()
