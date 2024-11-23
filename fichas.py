import math
import pygame
import sys
import utils
import jugadors as j
import jugadors_dades as jd
# Inicialización de Pygame y configuración de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

jugadors = j.jugadors


def dibuixar_fitxes(screen,idx):
    y = 400
    fitxes_actuals = jugadors[idx]["fitxes"]
    color_actual = jd.color(idx)
    
    for key,value in fitxes_actuals.items():
        if value > 0:
            pygame.draw.circle(screen,color_actual,(800,y),20)
            font = pygame.font.Font(None, 24)
            text = font.render(str(key), True, BLACK)
            quantitat = font.render(f"x{value}"  , True, WHITE)
            screen.blit(text, (800 - text.get_width() // 2, y - text.get_height() // 2))
            screen.blit(quantitat, (835 - text.get_width() // 2, y - text.get_height() // 2))
            y += 50
            