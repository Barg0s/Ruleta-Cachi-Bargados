import math
import pygame
import sys
import jugadors as j
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
TARONJA = (255,128,0) 
LILA = (204,169,221)
BLAU = (50, 120, 200)
idx = 0

def color(idx):
    colors = [TARONJA,LILA,BLAU]
    idx = idx % len(colors)  
    return colors[idx]      
        
def gestio_turns(screen, font, jugadors, idx,apostar):
    jugador_actual = jugadors[idx]['nom']
    color_actual = color(idx)

    jugador_text = font.render(f"Jugador {jugador_actual}", True, BLACK)
    diners_jugador = jugadors[idx]['diners']
    diners_text = font.render(f"Saldo: {diners_jugador}",True,BLACK)
    pygame.draw.rect(screen, color_actual, (700, 50, 150, 50))    
    screen.blit(jugador_text, (700, 50))
    screen.blit(diners_text,(700,75))
    if apostar:
        # Pasar al siguiente jugador
        idx += 1
        if idx >= len(jugadors): 
            idx = 0
        
        return idx  

