import pygame
import sys

# Inicializar Pygame
pygame.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Dimensiones de la ventana
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ventana Principal")

surface = pygame.Surface((screen_width, screen_height))

# Crear botones
button_width = 200
button_height = 50

# Botón para abrir la Surface (en la esquina superior izquierda)
open_button_rect = pygame.Rect(10, 10, button_width, button_height)

# Botón para cerrar la Surface (en la esquina superior derecha)
close_button_rect = pygame.Rect(screen_width - button_width - 10, 10, button_width, button_height)

# Bucle principal
running = True
show_surface = False  # La Surface comienza oculta
while running:
    screen.fill(BLACK)
    
    # Dibujar el botón de abrir si la Surface está oculta
    if not show_surface:
        pygame.draw.rect(screen, GREEN, open_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Abrir Surface", True, WHITE)
        screen.blit(text, (open_button_rect.x + 30, open_button_rect.y + 10))
    
    # Dibujar el botón de cerrar si la Surface está visible
    if show_surface:
        # Mostrar la Surface dentro de la ventana principal
        screen.blit(surface, (0, 0))  # La Surface ahora ocupa toda la ventana
        surface.fill(WHITE)  # Llenar la Surface con blanco (puedes personalizar esto)
        
        pygame.draw.rect(screen, RED, close_button_rect)
        text = font.render("Cerrar Surface", True, WHITE)
        screen.blit(text, (close_button_rect.x + 20, close_button_rect.y + 10))

    # Comprobamos eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Botón izquierdo del ratón
            if open_button_rect.collidepoint(event.pos) and not show_surface:  # Si se hace clic en el botón "Abrir"
                show_surface = True  # Mostrar la Surface
            if close_button_rect.collidepoint(event.pos) and show_surface:  # Si se hace clic en el botón "Cerrar"
                show_surface = False  # Ocultar la Surface

    pygame.display.flip()

# Cerrar Pygame correctamente
pygame.quit()
sys.exit()
