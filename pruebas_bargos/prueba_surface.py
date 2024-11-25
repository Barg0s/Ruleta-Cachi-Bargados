#!/usr/bin/env python3

import pygame
import sys
import utils

# Inicialización de Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 200)
RED = (255, 0, 0)  
GREEN = (0, 255, 0)
MARRON = (151, 91, 57)
GOLD = (255, 215, 0)
CENICA = (138, 149, 151)
VERDE = (0, 100, 0)

# Definir la ventana
screen = pygame.display.set_mode((860, 680))
pygame.display.set_caption('Window Title')

# Fuente para texto
font = pygame.font.SysFont("Arial", 22)
mouse = {'x': 1, 'y': -1}
# Botones generales
button_general = [
    {'name': 'Abrir', 'x': 500, 'y': 400, 'width': 100, 'height': 50, 'action': 'open'},
]
button_especial = [
    {'name': 'Cerrar', 'x': 550, 'y': 100, 'width': 50, 'height': 30, 'action': 'close'},
]
ventana_oberta = False

# Función para dibujar una ventana emergente
def dibujar_surface():
    global ventana_oberta
    if ventana_oberta:
        # Crear una nueva Surface para la ventana emergente
        surface = pygame.Surface((500, 400))  # Tamaño de la ventana emergente
        surface.fill(WHITE)  # Color de fondo de la ventana emergente

        # Dibujar un borde alrededor de la ventana
        pygame.draw.rect(surface, BLACK, (0, 0, 400, 300), 5)

        # Agregar texto dentro de la ventana emergente
        texto_surface = font.render("¡Ventana abierta!", True, BLUE)
        surface.blit(texto_surface, (400 // 2 - texto_surface.get_width() // 2, 100))

        # Dibujar el botón pequeño para cerrar la ventana
        for button in button_especial:
            pygame.draw.rect(screen, RED, (button['x'], button['y'], button['width'], button['height']))
            texto_cerrar = font.render("Cerrar", True, WHITE)
            surface.blit(texto_cerrar, (350 + (50 - texto_cerrar.get_width()) // 2, 50 + (30 - texto_cerrar.get_height()) // 2))

        # Mostrar la Surface en la pantalla principal en una ubicación específica
            screen.blit(surface, (430,340))  # Coloca la Surface en (200, 150) de la pantalla principal

        return surface  # Retornamos la Surface para usarla más tarde

# Función principal
def main():
    is_looping = True

    while is_looping:
        is_looping = app_events()
        app_run()
        app_draw()

        # Limitar a 60 FPS
        pygame.display.update()
        clock.tick(60) 

    # Cerrar el juego
    pygame.quit()
    sys.exit()

# Gestionar eventos
def app_events():
    global ventana_oberta, mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Botón cerrar ventana
            return False
        if event.type == pygame.MOUSEMOTION:
            mouse['x'], mouse['y'] = event.pos  # Actualizar la posición del ratón
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in button_general + button_especial:
                if utils.is_point_in_rect(mouse, button):  # Verificar si el clic está dentro de un botón
                    if button['action'] == 'open':
                        ventana_oberta = True  # Abrir ventana emergente
                    elif button['action'] == 'close':
                        ventana_oberta = False  # Cerrar ventana emergente
    return True

# Realizar cálculos
def app_run():
    pass

# Dibujar
def app_draw():
    screen.fill(WHITE)

    # Dibujar los botones
    for button in button_general:
        text_girar = font.render(button['name'], True, WHITE)
        pygame.draw.rect(screen, MARRON, (button['x'], button['y'], button['width'], button['height']))
        pygame.draw.rect(screen, BLACK, (button['x'], button['y'], button['width'], button['height']), 5)
        screen.blit(text_girar, (button['x'] + (button['width'] - text_girar.get_width()) // 2, button['y'] + (button['height'] - text_girar.get_height()) // 2))

    # Dibujar la ventana emergente si está abierta
    dibujar_surface()

# Iniciar la aplicación
if __name__ == "__main__":
    clock = pygame.time.Clock()
    main()
