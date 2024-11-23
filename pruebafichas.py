import math
import pygame
import sys
import utils
# Inicialización de Pygame y configuración de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
pygame.init()
clock = pygame.time.Clock()

# Configuración de la ventana y parámetros
screen = pygame.display.set_mode((860, 680))
pygame.display.set_caption('Roulette Game')

# Configuración de fichas apiladas
chip_templates = [
    {'value': 5, 'color': RED, 'x': 750, 'y': 100, 'radius': 20},
    {'value': 10, 'color': BLUE, 'x': 750, 'y': 200, 'radius': 20},
    {'value': 25, 'color': GREEN, 'x': 750, 'y': 300, 'radius': 20},
    {'value': 100, 'color': BLACK, 'x': 750, 'y': 400, 'radius': 20},
]

chips = []  # Lista para todas las fichas activas en el tablero

# Variables de control para arrastrar fichas
dragging_chip = None  # Indica qué ficha se está arrastrando
offset_x, offset_y = 0, 0  # Compensación entre el clic y el centro de la ficha

# Función para agregar fichas apiladas
def add_chips(value, color, x, y, radius, quantity=5):
    # Crear fichas apiladas
    for i in range(quantity):
        chips.append({'value': value, 'color': color, 'x': x, 'y': y + i * 5, 'radius': radius})

# Crear las 5 fichas apiladas para cada valor solo al inicio
for template in chip_templates:
    add_chips(template['value'], template['color'], template['x'], template['y'], template['radius'], 5)

# Eventos del programa principal
def app_events():
    global dragging_chip, offset_x, offset_y
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Verificar si se hace clic en alguna ficha del tablero para arrastrarla
            for chip in chips:
                if utils.is_point_in_circle({"x": mouse_pos[0], "y": mouse_pos[1]}, {"x": chip['x'], "y": chip['y']}, chip['radius']):
                    dragging_chip = chip
                    offset_x = chip['x'] - mouse_pos[0]
                    offset_y = chip['y'] - mouse_pos[1]
                    break

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_chip = None  # Deja de arrastrar la ficha

        elif event.type == pygame.MOUSEMOTION and dragging_chip:
            # Actualiza la posición de la ficha mientras se arrastra
            mouse_pos = pygame.mouse.get_pos()
            dragging_chip['x'] = mouse_pos[0] + offset_x
            dragging_chip['y'] = mouse_pos[1] + offset_y

# Dibuja las fichas en la pantalla
def draw_chips():
    # Dibujar las fichas de la columna de fichas iniciales
    for template in chip_templates:
        pygame.draw.circle(screen, template['color'], (template['x'], template['y']), template['radius'])
        font = pygame.font.Font(None, 24)
        text = font.render(str(template['value']), True, BLACK if template['color'] != BLACK else WHITE)
        screen.blit(text, (template['x'] - text.get_width() // 2, template['y'] - text.get_height() // 2))

    # Dibujar las fichas activas en el tablero
    for chip in chips:
        pygame.draw.circle(screen, chip['color'], (chip['x'], chip['y']), chip['radius'])
        font = pygame.font.Font(None, 24)
        text = font.render(str(chip['value']), True, BLACK if chip['color'] != BLACK else WHITE)
        screen.blit(text, (chip['x'] - text.get_width() // 2, chip['y'] - text.get_height() // 2))

# Dibuja el contenido de la aplicación
def app_draw():
    screen.fill(WHITE)
    draw_chips()
    pygame.display.flip()

# Bucle principal de la aplicación
def main():
    while True:
        app_events()
        app_draw()
        clock.tick(60)

if __name__ == "__main__":
    main()
