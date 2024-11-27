# principal.py

import pygame
import sys
from surface import *

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 860
SCREEN_HEIGHT = 680

# Inicializar pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Scroll Test")

# Crear el rectángulo de cierre
close_button_rect = {"x": SCREEN_WIDTH - 60, "y": 10, "width": 50, "height": 25}

# Bucle principal
def main():
    mouse = {"x": 0, "y": 0, "pressed": False}
    show_surface = True

    while True:
        screen.fill(WHITE)
        mouse["x"], mouse["y"] = pygame.mouse.get_pos()

        # Manejar eventos de ratón y actualizar el estado del scroll
        show_surface = events_surface(mouse, close_button_rect, show_surface)

        # Dibujar todo en la pantalla
        draw_surface()
        draw_scroll_slider()
        draw_close_button(close_button_rect)

        # Actualizar la posición del scroll
        update_scroll_position(mouse)

        pygame.display.update()

if __name__ == "__main__":
    main()
