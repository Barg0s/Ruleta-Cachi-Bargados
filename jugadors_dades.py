import math
import pygame
import sys
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
    pygame.draw.rect(screen, color_actual, (50, 50, 150, 50))    
    screen.blit(jugador_text, (50, 50))
    screen.blit(diners_text,(50,75))
    if apostar:
        # Pasar al siguiente jugador
        idx += 1
        if idx >= len(jugadors): 
            idx = 0
        
        return idx  

def dibuixar_banca(screen,font,banca):
    jugador_text = font.render("BANCA", True, BLACK)
    diners_banca = banca['diners']
    diners_text = font.render(f"Saldo: {diners_banca}",True,BLACK)
    pygame.draw.rect(screen, WHITE, (400, 50, 150, 50))    
    screen.blit(jugador_text, (450, 50))
    screen.blit(diners_text,(435,75))


def sumar_banca(jugadors,banca):
        diners_banca = banca['diners']
        for jugador in jugadors:
            valors = int(jugador['value'])
            diners_banca += valors