import pygame
import sys
import tauler as t
import jugadors as j
import utils

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (50, 120, 200)

# Inicialización de Pygame
pygame.init()
clock = pygame.time.Clock()

# Configuración de pantalla
screen = pygame.display.set_mode((860, 680))
pygame.display.set_caption('Roulette Game')

# Variables globales
chips = []
apuestas = []
mouse = {'x': -1, 'y': -1}

# Tablero de apuestas
carton_pos = (100, 450)
carton_casilla_ancho = 50
carton_casilla_alto = 50
carton_filas = 3
carton_columnas = 12
betting_table = [
    [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
    [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
    [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
]

# Jugadores
jugadors = j.jugadors
turno_actual = 0

# Botones
boton_rect = pygame.Rect(700, 20, 140, 40)

# Variables de arrastre
dragging_chip = None
offset_x, offset_y = 0, 0

def add_chips_for_current_player():
    """Añade las fichas del jugador actual."""
    global chips
    chips = []
    jugador = jugadors[turno_actual]
    x_base = 800
    y_base = 400
    radius = 20
    y_spacing = 5
    for valor, cantidad in jugador["fitxes"].items():
        y = y_base
        for _ in range(cantidad):
            chips.append({'value': int(valor), 'color': jugador["color"], 'x': x_base, 'y': y, 'radius': radius, 'owner': jugador["nom"]})
            y += y_spacing
        y_base += 60

def app_events():
    """Gestiona eventos de la aplicación."""
    global turno_actual, dragging_chip, offset_x, offset_y
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if boton_rect.collidepoint(mouse_pos):
                turno_actual = (turno_actual + 1) % len(jugadors)
                add_chips_for_current_player()
            for chip in chips:
                if utils.is_point_in_circle({'x': mouse_pos[0], 'y': mouse_pos[1]}, {'x': chip['x'], 'y': chip['y']}, chip['radius']):
                    dragging_chip = chip
                    offset_x = mouse_pos[0] - chip['x']
                    offset_y = mouse_pos[1] - chip['y']
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_chip:
                # Verificar casillas normales
                for button in t.betting_buttons:
                    if utils.is_point_in_rect({'x': dragging_chip['x'], 'y': dragging_chip['y']}, button):
                        col = (button['x'] - carton_pos[0]) // carton_casilla_ancho
                        row = (button['y'] - carton_pos[1]) // carton_casilla_alto
                        pos = row * carton_columnas + col
                        jugador = next(jugador for jugador in jugadors if jugador["nom"] == dragging_chip["owner"])
                        jugador["fitxes"][str(dragging_chip['value'])] -= 1
                        x_pos = carton_pos[0] + col * carton_casilla_ancho + carton_casilla_ancho // 2
                        y_pos = carton_pos[1] + row * carton_casilla_alto + carton_casilla_alto // 2
                        dragging_chip['x'] = x_pos
                        dragging_chip['y'] = y_pos
                        apuestas.append({'jugador': dragging_chip['owner'], 'posicion': pos, 'value': dragging_chip['value'], 'color': dragging_chip['color']})

                        numero = betting_table[row][col]
                        print(f"Ficha colocada por {dragging_chip['owner']} en el número {numero}")
                        chips.remove(dragging_chip)
                        break
                else:
                    # Verificar casillas especiales
                    for button in t.custom_buttons:
                        if utils.is_point_in_rect({'x': dragging_chip['x'], 'y': dragging_chip['y']}, button):
                            print(f"Ficha colocada en {button['label']} por {dragging_chip['owner']}")
                            dragging_chip['x'] = button['x'] + button['width'] // 2
                            dragging_chip['y'] = button['y'] + button['height'] // 2
                            apuestas.append({'jugador': dragging_chip['owner'], 'posicion': -1, 'value': dragging_chip['value'], 'color': dragging_chip['color'], 'label': button['label']})
                            chips.remove(dragging_chip)
                            break
                    else:
                        dragging_chip['x'], dragging_chip['y'] = 200, 150
                dragging_chip = None
        elif event.type == pygame.MOUSEMOTION and dragging_chip:
            mouse_pos = pygame.mouse.get_pos()
            dragging_chip['x'] = mouse_pos[0] - offset_x
            dragging_chip['y'] = mouse_pos[1] - offset_y

def draw_chips():
    """Dibuja las fichas activas."""
    for chip in chips:
        pygame.draw.circle(screen, chip['color'], (chip['x'], chip['y']), chip['radius'])
        font = pygame.font.Font(None, 24)
        text = font.render(str(chip['value']), True, BLACK if chip['color'] != BLACK else WHITE)
        screen.blit(text, (chip['x'] - text.get_width() // 2, chip['y'] - text.get_height() // 2))

def draw_apuestas():
    """Dibuja las fichas colocadas."""
    for apuesta in apuestas:
        if apuesta.get('posicion') >= 0:  # Para las casillas normales
            col = apuesta['posicion'] % carton_columnas
            row = apuesta['posicion'] // carton_columnas
            x = carton_pos[0] + col * carton_casilla_ancho + carton_casilla_ancho // 2
            y = carton_pos[1] + row * carton_casilla_alto + carton_casilla_alto // 2
        else:  # Para las casillas especiales
            button = next(b for b in t.custom_buttons if b['label'] == apuesta['label'])
            x = button['x'] + button['width'] // 2
            y = button['y'] + button['height'] // 2
        pygame.draw.circle(screen, apuesta['color'], (x, y), 20)
        font = pygame.font.Font(None, 24)
        text = font.render(str(apuesta['value']), True, BLACK if apuesta['color'] != BLACK else WHITE)
        screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

def main():
    """Bucle principal del juego."""
    global screen, turno_actual
    add_chips_for_current_player()
    while True:
        screen.fill(DARK_GRAY)
        app_events()
        t.draw_betting_buttons(screen)  # Tablero de apuestas
        t.draw_custom_buttons(screen)  # Botones especiales
        draw_apuestas()               # Fichas colocadas
        draw_chips()                  # Fichas activas
        pygame.draw.rect(screen, BLUE, boton_rect)
        font = pygame.font.Font(None, 24)
        text = font.render(f"Jugador: {jugadors[turno_actual]['nom']}", True, WHITE)
        screen.blit(text, (20, 20))
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
