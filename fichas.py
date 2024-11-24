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
carton_pos = (100, 450)
carton_casilla_ancho = 50
carton_casilla_alto = 50
carton_filas = 3
carton_columnas = 12
apuestas = []

jugadors = j.jugadors

chips = []


def afegir_fitxes(idx):
    global chips
    chips = []
    jugador = jugadors[idx]
    x_base = 800
    y_base = 400
    radius = 20
    y_spacing = 2
    for valor, cantidad in jugador["fitxes"].items():
        y = y_base
        for _ in range(cantidad):
            chips.append({'value': int(valor), 'color': jugador["color"], 'x': x_base, 'y': y, 'radius': radius, 'owner': jugador["nom"]})
            y += y_spacing
        y_base += 60



def dibuixar_fitxes(screen):
    # Dibujar todas las fichas
    for chip in chips:
        for button in t.custom_buttons:
            button_rect = pygame.Rect(button['x'], button['y'], button['width'], button['height'])
            if button_rect.collidepoint(chip['x'], chip['y']):
                pygame.draw.circle(screen, chip['color'], (chip['x'], chip['y']), chip['radius'])
                font = pygame.font.Font(None, 24)
                text = font.render(str(chip['value']), True, BLACK if chip['color'] != BLACK else WHITE)
                screen.blit(text, (chip['x'] - text.get_width() // 2, chip['y'] - text.get_height() // 2))
                break
        else:
            pygame.draw.circle(screen, chip['color'], (chip['x'], chip['y']), chip['radius'])
            font = pygame.font.Font(None, 24)
            text = font.render(str(chip['value']), True, BLACK if chip['color'] != BLACK else WHITE)
            screen.blit(text, (chip['x'] - text.get_width() // 2, chip['y'] - text.get_height() // 2))

