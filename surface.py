import pygame
import sys

# Inicializar Pygame
pygame.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
button_width = 200
button_height = 50
close_button_rect = pygame.Rect(SCREEN_WIDTH - button_width - 10, 10, button_width, button_height)
show_surface = False

def dibuixar_surface(screen,font,show_surface):
    if show_surface:
        screen.blit(surface,(0,0))
        surface.fill(WHITE)
        pygame.draw.rect(screen, RED, close_button_rect)
        text = font.render("Cerrar Surface", True, WHITE)
        screen.blit(text, (close_button_rect.x + 20, close_button_rect.y + 10))

    for event in pygame.event.get():
        if close_button_rect.collidepoint(event.pos) and show_surface:  # Si se hace clic en el botón "Cerrar"
            show_surface = False  # Ocultar la Surface
